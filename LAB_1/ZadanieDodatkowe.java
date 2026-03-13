import java.awt.*;
import java.io.*;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.*;
import java.util.List;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.function.Function;
import java.util.stream.Collectors;
import javax.swing.*;
import java.util.stream.Stream;


public class ZadanieDodatkowe {
    private JFrame frame;
    private static final String DIR_PATH = "src/files"; // Tu leżą pliki
    private static final Path MASTER_FILE = Paths.get("src/files/wzorzec.txt"); // To jest wzorzec

    private final AtomicBoolean fajrant = new AtomicBoolean(false); // Flaga, żeby wiedzieć, kiedy fajrant
    private final int liczbaProducentow = 1;
    private final int liczbaKonsumentow = 2;
    // Pula wątków, żeby system nie wywalił od nadmiaru procesów
    private final ExecutorService executor = Executors.newFixedThreadPool(liczbaProducentow + liczbaKonsumentow);
    private final List<Future<?>> producentFuture = new ArrayList<>();

    // Mapa słów wzorca - ładowana raz, żeby nie mielić dysku bez sensu
    private Map<String, Long> masterVector;

    public static void main(String[] args) {
        //Dajemy ładne GUI bo why not?
        try { UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName()); } catch (Exception ignored) {}
        EventQueue.invokeLater(() -> {
            try {
                new SimilarityFrame().frame.setVisible(true);
            } catch (Exception e) { e.printStackTrace(); }
        });
    }

    public SimilarityFrame() {
        // Na start wczytuj wzorzec, żeby potem w wątkach był już gotowy
        this.masterVector = loadVector(MASTER_FILE);
        initialize();
    }

    private void initialize() {
        frame = new JFrame("Analizator Podobieństwa Kosinusowego");
        frame.setBounds(100, 100, 500, 400);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JPanel panel = new JPanel();
        JButton btnStart = new JButton("Start Analizy");
        JButton btnStop = new JButton("Stop");

        panel.add(btnStart);
        panel.add(btnStop);
        frame.getContentPane().add(panel, BorderLayout.NORTH);

        JTextArea textArea = new JTextArea();
        frame.getContentPane().add(new JScrollPane(textArea), BorderLayout.CENTER);

        btnStart.addActionListener(e -> startAnalysis(textArea));
        btnStop.addActionListener(e -> stopAnalysis());
    }

    private void startAnalysis(JTextArea output) {
        if (masterVector.isEmpty()) {
            JOptionPane.showMessageDialog(frame, "Błąd: Plik wzorcowy 'wzorzec.txt' jest pusty lub nie istnieje!");
            return;
        }

        fajrant.set(false);
        output.setText("Rozpoczynanie analizy...\n");

        // Kolejka na 5 slotów - jak konsumenci zamulą, producent poczeka
        final BlockingQueue<Optional<Path>> kolejka = new LinkedBlockingQueue<>(5);

        // --- PRODUCENT --- (gość od szukania po folderach)
        Runnable producent = () -> {
            try {
                Files.walkFileTree(Paths.get(DIR_PATH), new SimpleFileVisitor<>() {
                    @Override
                    public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
                        // Szukamy tekstówek, ale omijamy sam wzorzec
                        if (file.toString().endsWith(".txt") && !file.equals(MASTER_FILE)) {
                            try {
                                if (fajrant.get()) return FileVisitResult.TERMINATE;
                                // Wrzuć ścieżkę do kolejki
                                kolejka.put(Optional.of(file));
                            } catch (InterruptedException e) { return FileVisitResult.TERMINATE; }
                        }
                        return FileVisitResult.CONTINUE;
                    }
                });
            } catch (IOException e) { e.printStackTrace(); }
            finally {
                // Koniec roboty? Wysyłamy "pigułki śmierci", żeby konsumenci wiedzieli, że czas się zwijać
                for (int i = 0; i < liczbaKonsumentow; i++) {
                    try { kolejka.put(Optional.empty()); } catch (InterruptedException ignored) {}
                }
            }
        };

        // --- KONSUMENT --- (gość od czarnej roboty i zliczania)
        Runnable konsument = () -> {
            while (true) {
                try {
                    // Wyciągnij coś z kolejki (albo śpij, jak jest pusta)
                    Optional<Path> optPath = kolejka.take();
                    if (optPath.isEmpty()) break; // Trafiliśmy na pigułkę śmierci -> kończymy wątek

                    Path path = optPath.get();
                    double similarity = calculateCosine(path);

                    // Update UI musi lecieć przez invokeLater, bo Swing nie jest thread-safe
                    SwingUtilities.invokeLater(() ->
                            output.append(String.format("Plik: %s -> Podobieństwo: %.2f%%\n",
                                    path.getFileName(), similarity * 100)));

                } catch (InterruptedException e) { Thread.currentThread().interrupt(); break; }
            }
        };

        // Odpalamy ekipę przez executor
        producentFuture.add(executor.submit(producent));
        for (int i = 0; i < liczbaKonsumentow; i++) executor.execute(konsument);
    }

    private void stopAnalysis() {
        fajrant.set(true); // Sygnał dla producenta, żeby przestał szukać
        for (Future<?> f : producentFuture) f.cancel(true); // Przerwij mu robotę siłą, jak trzeba
        producentFuture.clear();
    }

    // Pomocnicza metoda do robienia "mapy słów" z pliku
    private Map<String, Long> loadVector(Path path) {
        if (!Files.exists(path)) return Collections.emptyMap();
        try (Stream<String> lines = Files.lines(path)) {
            return lines.flatMap(line -> Arrays.stream(line.split("\\s+")))
                    .map(word -> word.toLowerCase().replaceAll("[^a-z0-9ąęóśćżńź]", "")) // Czyścimy syf
                    .filter(word -> word.length() >= 3) // Krótkie spójniki nas nie obchodzą
                    .collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));
        } catch (IOException e) { return Collections.emptyMap(); }
    }

    // Liczymy cosinusa - im bliżej 1, tym bardziej pliki są podobne
    private double calculateCosine(Path targetPath) {
        Map<String, Long> targetVector = loadVector(targetPath);
        if (targetVector.isEmpty()) return 0.0;

        // Robimy zestaw wszystkich słów z obu plików
        Set<String> both = new HashSet<>(masterVector.keySet());
        both.addAll(targetVector.keySet());

        double dotProduct = 0, normA = 0, normB = 0;

        for (String word : both) {
            long freqA = masterVector.getOrDefault(word, 0L);
            long freqB = targetVector.getOrDefault(word, 0L);

            // Klasyka: iloczyn skalarny i kwadraty do długości wektorów
            dotProduct += freqA * freqB;
            normA += Math.pow(freqA, 2);
            normB += Math.pow(freqB, 2);
        }

        // Dzielenie przez zero to zło, więc sprawdzamy normy
        return (normA == 0 || normB == 0) ? 0.0 : dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
    }
}