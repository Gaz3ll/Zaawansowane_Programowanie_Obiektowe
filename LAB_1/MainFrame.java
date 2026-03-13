import java.awt.BorderLayout;
import java.awt.EventQueue;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.function.Function;
import java.util.stream.Collectors;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.UIManager;

public class MainFrame {
    private JFrame frame;
    private static final String DIR_PATH = "src/files"; // Ścieżka do katalogu z plikami
    private final int liczbaWyrazowStatystyki;
    private final AtomicBoolean fajrant; // Flaga, żeby wiedzieć, kiedy fajrant
    private final int liczbaProducentow;
    private final int liczbaKonsumentow;


    private ExecutorService executor;// Flaga, żeby wiedzieć, kiedy fajrant
    // Pula wątków, żeby system nie wywalił od nadmiaru procesów
    private List<Future<?>> producentFuture;

    public static void main(String[] args) {
        //Dajemy ładne GUI bo why not?
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            e.printStackTrace();
        }
        // Uruchomienie interfejsu graficznego
        EventQueue.invokeLater(() -> {
            try {
                MainFrame window = new MainFrame();
                window.frame.pack();
                window.frame.setVisible(true);
            } catch (Exception e) {
                e.printStackTrace();
            }
        });
    }

    public MainFrame() {
        liczbaWyrazowStatystyki = 10;
        fajrant = new AtomicBoolean(false);
        liczbaProducentow = 1;
        liczbaKonsumentow = 2;

        // Rezerwujemy miejsce dla producentów i konsumentów w puli
        executor = Executors.newFixedThreadPool(liczbaProducentow + liczbaKonsumentow);
        producentFuture = new ArrayList<>();
        initialize();
    }

    private void initialize() {
        frame = new JFrame("Analizator Plików");
        frame.addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent e) {
                // Zamykasz okno -> ucinamy wszystkie wątki od razu
                executor.shutdownNow();
            }
        });
        frame.setBounds(100, 100, 450, 300);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JPanel panel = new JPanel();
        frame.getContentPane().add(panel, BorderLayout.NORTH);

        JButton btnStart = new JButton("Start");
        btnStart.addActionListener(e -> getMultiThreadedStatistics());

        JButton btnStop = new JButton("Stop");
        btnStop.addActionListener(e -> {
            fajrant.set(true); // Ej producent kończ skanować fajrant mamy
            for (Future<?> f : producentFuture) {
                f.cancel(true); // Ci co śpią też kończą
            }
        });

        JButton btnZamknij = new JButton("Zamknij");
        btnZamknij.addActionListener(e -> {
            executor.shutdownNow();
            frame.dispose();
        });

        panel.add(btnStart);
        panel.add(btnStop);
        panel.add(btnZamknij);
    }

    private void getMultiThreadedStatistics() {
        // Żeby nie napierdzielać startu kilka razy bo się program może wieszać. Po co zapierniczać podwójnie
        for (Future<?> f : producentFuture) {
            if (!f.isDone()) {
                JOptionPane.showMessageDialog(frame, "Producent nadal działa!", "OSTRZEŻENIE", JOptionPane.WARNING_MESSAGE);
                return;
            }
        }

        fajrant.set(false);
        producentFuture.clear();

        // Kolejka blokująca o rozmiarze 5 - jeśli będzie pełna, producent poczeka
        // Optional.empty() służy jako Poison Pill (sygnał końca pracy)
        final BlockingQueue<Optional<Path>> kolejka = new LinkedBlockingQueue<>(5);
        final int przerwa = 10; // Czas oczekiwania producenta między skanowaniami

        //DEFINICJA PRODUCENTA - Wyszukiwanie plików
        Runnable producent = () -> {
            final String name = Thread.currentThread().getName();
            System.out.println("PRODUCENT " + name + " URUCHOMIONY...");

            try {
                while (!Thread.currentThread().isInterrupted() && !fajrant.get()) {
                    // Rekurencyjne przeszukiwanie drzewa katalogów
                    Files.walkFileTree(Paths.get(DIR_PATH), new SimpleFileVisitor<Path>() {
                        @Override
                        public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
                            if (file.toString().endsWith(".txt")) {
                                try {
                                    // Wstawienie pliku do kolejki, blokuje wątek, jeśli kolejka jest pełna
                                    kolejka.put(Optional.of(file));
                                    System.out.println("Producent dodał: " + file.getFileName());
                                } catch (InterruptedException e) {
                                    return FileVisitResult.TERMINATE;
                                }
                            }
                            return fajrant.get() ? FileVisitResult.TERMINATE : FileVisitResult.CONTINUE;
                        }
                    });

                    System.out.println("Producent " + name + " idzie spać na " + przerwa + "s.");
                    TimeUnit.SECONDS.sleep(przerwa);
                }
            } catch (IOException | InterruptedException e) {
                System.out.println("Producent " + name + " przerwany.");
            } finally {
                // Po zakończeniu pętli, wyślij sygnał końca dla każdego konsumenta
                for (int i = 0; i < liczbaKonsumentow; i++) {
                    try {
                        kolejka.put(Optional.empty());
                    } catch (InterruptedException ignored) {}
                }
                System.out.println("PRODUCENT " + name + " SKOŃCZYŁ PRACĘ");
            }
        };

        //DEFINICJA KONSUMENTA - Przetwarzanie treści plików
        Runnable konsument = () -> {
            final String name = Thread.currentThread().getName();
            System.out.println("KONSUMENT " + name + " URUCHOMIONY...");

            while (true) {
                try {
                    // Pobranie elementu z kolejki, blokuje wątek, jeśli kolejka jest pusta
                    Optional<Path> optPath = kolejka.take();

                    if (optPath.isPresent()) {
                        Path path = optPath.get();
                        // Wykonanie ciężkich obliczeń statystycznych
                        Map<String, Long> stats = getLinkedCountedWords(path, liczbaWyrazowStatystyki);
                        System.out.println(name + " przetworzył " + path.getFileName() + ": " + stats);
                    } else {
                        // Odebrano Optional.empty() - sygnał do zakończenia pracy wątku
                        break;
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt(); // Przywrócenie flagi przerwania
                    break;
                }
            }
            System.out.println("KONSUMENT " + name + " ZAKOŃCZYŁ PRACĘ");
        };

        // Zlecenie zadań do puli egzekutora
        for (int i = 0; i < liczbaProducentow; i++) {
            producentFuture.add(executor.submit(producent));
        }
        for (int i = 0; i < liczbaKonsumentow; i++) {
            executor.execute(konsument);
        }
    }

    /**
     * Logika analizy tekstu z użyciem Java Streams.
     */
    private Map<String, Long> getLinkedCountedWords(Path path, int wordsLimit) {
        try (BufferedReader reader = Files.newBufferedReader(path)) {
            return reader.lines() // Odczyt linii po linii (wydajne pamięciowo)
                    .flatMap(line -> Arrays.stream(line.split("\\s+"))) // Podział na słowa
                    .map(word -> word.toLowerCase().replaceAll("[^a-z0-9ąęóśćżńź]", "")) // Wszystko spoza regexu weź wywal bo zbędne
                    .filter(word -> word.length() >= 3) // Odrzucenie wyrazów krótszych niż 3 znaki (min. 3)
                    .collect(Collectors.groupingBy(Function.identity(), Collectors.counting())) // Liczenie ile razy się pojawiło
                    .entrySet().stream()
                    .sorted(Map.Entry.comparingByValue(Comparator.reverseOrder())) // Sortuj od największej ilości pojawień
                    .limit(wordsLimit) // Ograniczenie wyników do 10
                    .collect(Collectors.toMap(
                            Map.Entry::getKey,
                            Map.Entry::getValue,
                            (v1, v2) -> v1,
                            LinkedHashMap::new // Zachowanie kolejności sortowania w wynikowej mapie
                    ));
        } catch (IOException e) {
            System.err.println("Błąd odczytu pliku: " + path);
            return Collections.emptyMap();
        }
    }
}