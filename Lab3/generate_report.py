#!/usr/bin/env python3
"""Generate a PDF lab report matching the style of ZPO_LAB3_Leśniewski_Wiktor.pdf."""

from fpdf import FPDF

FONT_DIR = "C:/Windows/Fonts"


class LabReport(FPDF):
    """Custom PDF with Times New Roman + Consolas, matching reference style."""

    def __init__(self):
        super().__init__()
        self.add_font("TNR", "", f"{FONT_DIR}/times.ttf")
        self.add_font("TNR", "B", f"{FONT_DIR}/timesbd.ttf")
        self.add_font("TNR", "I", f"{FONT_DIR}/timesi.ttf")
        self.add_font("TNR", "BI", f"{FONT_DIR}/timesbi.ttf")
        self.add_font("Consolas", "", f"{FONT_DIR}/consola.ttf")
        self.add_font("Consolas", "B", f"{FONT_DIR}/consolab.ttf")

    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("TNR", "I", 10)
        self.cell(0, 10, f"Strona {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.set_font("TNR", "B", 12)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def body_text(self, text):
        self.set_font("TNR", "", 12)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def code_block(self, code):
        self.set_fill_color(245, 245, 245)
        self.set_draw_color(210, 210, 210)
        self.set_font("Consolas", "", 9)
        lines = code.split("\n")
        bh = len(lines) * 4.5 + 4
        if self.get_y() + bh > 260:
            self.add_page()
        x = self.get_x()
        y = self.get_y()
        self.rect(x, y, 190, bh, style="DF")
        self.set_xy(x + 3, y + 2)
        for line in lines:
            self.cell(0, 4.5, line.replace("\t", "    "), new_x="LMARGIN", new_y="NEXT")
            self.set_x(x + 3)
        self.ln(4)

    def inline_code(self, text):
        """Use Consolas within a sentence (caller must handle font switching)."""
        self.set_font("Consolas", "", 12)
        self.write(5.5, text)
        self.set_font("TNR", "", 12)

    def label_value(self, label, value, x1=30, x2=70):
        """Print a label: value pair on the same line."""
        self.set_font("TNR", "B", 12)
        self.cell(45, 7, label + " ")
        self.set_font("TNR", "", 12)
        self.cell(0, 7, str(value), new_x="LMARGIN", new_y="NEXT")


def build_report():
    pdf = LabReport()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # ===================== TITLE PAGE =====================
    pdf.ln(15)

    # University name
    pdf.set_font("TNR", "", 12)
    pdf.cell(0, 7, "Politechnika Bydgoska im. J. J. Sniadeckich", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("TNR", "B", 12)
    pdf.cell(0, 7, "Wydzial Telekomunikacji, Informatyki i Elektrotechniki", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    # Horizontal rule
    pdf.set_draw_color(0, 0, 0)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    pdf.ln(8)

    # Info table
    pdf.label_value("Przedmiot", "Zaawansowane Programowanie Obiektowe")
    pdf.label_value("Prowadzacy", "dr inz. Damian Szczegielniak")
    pdf.label_value("Temat", "Implementacja aplikacji bazodanowej przy uzyciu JDBC + JavaFX")

    pdf.ln(3)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    pdf.ln(5)

    pdf.label_value("Student", "Wiktor Lesniewski")
    pdf.label_value("Nr cw.", "3")
    pdf.label_value("Data wykonania", "maj 2026")
    pdf.label_value("Ocena", "")
    pdf.label_value("Data oddania spr.", "")

    pdf.ln(5)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    pdf.ln(6)

    # ===================== SECTION: OPIS PROBLEMU =====================
    pdf.section_title("Opis problemu do rozwiazania:")
    pdf.body_text(
        "Celem zadania bylo stworzenie w pelni funkcjonalnej aplikacji okienkowej w jezyku Java, "
        "laczacej sie z relacyjna baza danych HSQLDB za pomoca technologii JDBC. "
        "Aplikacja umozliwia wykonywanie operacji CRUD (Create, Read, Update, Delete) "
        "na dwoch powiazanych ze soba tabelach: 'projekt' oraz 'zadanie'. "
        "Dodatkowo zaimplementowano mechanizm logowania (SLF4J + Logback), "
        "zarzadzanie polaczeniami poprzez pule HikariCP oraz graficzny interfejs "
        "uzytkownika w technologii JavaFX z wykorzystaniem plikow FXML."
    )

    pdf.body_text(
        "W projekcie zaimplementowano nastepujace komponenty:"
    )

    # Use bullet-like listing
    items = [
        ("Model danych (", "Projekt", ", ", "Zadanie", ") - klasy Java odwzorowujace tabele bazy danych."),
        ("Pula polaczen - ", "DataSource", " (Singleton) oparta na ", "HikariCP", "."),
        ("Inicjalizacja bazy - ", "DbInitializer", " tworzacy strukture tabel, indeksow i kluczy obcych."),
        ("Warstwa DAO - interfejsy ", "ProjektDAO", ", ", "ZadanieDAO", " i ich implementacje z ", "PreparedStatement", "."),
        ("Interfejs graficzny - JavaFX z plikami FXML (", "ProjectFrame.fxml", ", ", "ZadanieFrame.fxml", ")."),
        ("Kontrolery - ", "ProjectController", ", ", "ZadanieController", " obslugujace zdarzenia GUI i logike biznesowa."),
        ("Logowanie - SLF4J + Logback z zapisem do pliku i archiwizacja."),
    ]
    for item in items:
        pdf.set_font("TNR", "", 12)
        parts = item
        i = 0
        while i < len(parts):
            if parts[i].startswith("(") and parts[i].endswith(")"):
                pdf.set_font("TNR", "", 12)
                pdf.write(5.5, parts[i])
            else:
                pdf.set_font("Consolas", "", 12)
                pdf.write(5.5, parts[i])
            i += 1
            if i < len(parts) and not (parts[i].startswith("(") and parts[i].endswith(")")):
                pdf.set_font("TNR", "", 12)
                pdf.write(5.5, parts[i])
                i += 1
        pdf.ln(6)

    pdf.ln(2)

    # ===================== SECTION: STRUKTURA PROJEKTU =====================
    pdf.add_page()
    pdf.section_title("Struktura projektu")
    pdf.code_block("""\
project-jfx-client/
+-- build.gradle
+-- settings.gradle
+-- src/main/java/
|   +-- module-info.java
|   +-- com/project/
|       +-- app/
|       |   +-- ProjectClientApplication.java
|       +-- controller/
|       |   +-- ProjectController.java
|       |   +-- ZadanieController.java
|       +-- dao/
|       |   +-- ProjektDAO.java
|       |   +-- ProjektDAOImpl.java
|       |   +-- ZadanieDAO.java
|       |   +-- ZadanieDAOImpl.java
|       +-- datasource/
|       |   +-- DataSource.java
|       |   +-- DbInitializer.java
|       +-- model/
|           +-- Projekt.java
|           +-- Zadanie.java
+-- src/main/resources/
    +-- css/application.css
    +-- fxml/ProjectFrame.fxml
    +-- fxml/ZadanieFrame.fxml
    +-- logback.xml""")

    # ===================== KONFIGURACJA =====================
    pdf.section_title("Konfiguracja projektu (build.gradle)")
    pdf.body_text(
        "Plik build.gradle okresla zaleznosci projektu: HSQLDB 2.7.4, HikariCP 6.2.1, "
        "Logback 1.5.17, SLF4J 2.0.17 oraz JavaFX 23.0.2. Ustawiono zgodnosc z Java 21 "
        "oraz okreslono modul glowny i klase uruchomieniowa."
    )
    pdf.code_block("""\
plugins {
    id 'application'  id 'java'  id 'eclipse'
    id 'org.openjfx.javafxplugin' version '0.1.0'
    id 'org.beryx.jlink' version '3.1.1'
}
group = 'com.project'  version = '1.0'
repositories { mavenCentral() }
dependencies {
    implementation 'org.hsqldb:hsqldb:2.7.4'
    implementation 'com.zaxxer:HikariCP:6.2.1'
    implementation 'ch.qos.logback:logback-classic:1.5.17'
    implementation 'ch.qos.logback:logback-core:1.5.17'
    implementation 'org.slf4j:slf4j-api:2.0.17'
}
java { sourceCompatibility = '21'  modularity.inferModulePath = true }
javafx {
    version = '23.0.2'
    modules = ['javafx.controls', 'javafx.fxml', 'javafx.base', 'javafx.graphics']
}
application {
    mainModule = 'project.jfx.client'
    mainClass = 'com.project.app.ProjectClientApplication'
}""")

    # ===================== MECHANIZM REJESTRACJI =====================
    pdf.section_title("Mechanizm rejestracji (Logback)")
    pdf.body_text(
        "Plik logback.xml definiuje dwa appenders: STDOUT (konsola) oraz FILE (plik z archiwizacja). "
        "Logger dla pakietu com.project zapisuje do obu, root wysyla tylko na konsole. "
        "Pliki logow sa archiwizowane dziennie, historia 30 dni (max 30 MB)."
    )
    pdf.code_block("""\
<configuration debug="true">
    <property name="LOG_FILE" value="project-jfx-client" />
    <property name="LOG_DIR" value="logs" />
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36}.%M\\(%line\\) - %msg%n</pattern>
        </encoder>
    </appender>
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${LOG_DIR}/${LOG_FILE}.log</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>${LOG_ARCHIVE}/%d{yyyy-MM-dd}${LOG_FILE}.log.zip</fileNamePattern>
            <maxHistory>30</maxHistory>
            <totalSizeCap>30MB</totalSizeCap>
        </rollingPolicy>
    </appender>
    <logger name="com.project" level="INFO" additivity="false">
        <appender-ref ref="STDOUT" /><appender-ref ref="FILE" />
    </logger>
    <root level="INFO"><appender-ref ref="STDOUT" /></root>
</configuration>""")

    # ===================== MODEL =====================
    pdf.add_page()
    pdf.section_title("Model danych - klasy Projekt i Zadanie")
    pdf.body_text(
        "W pakiecie com.project.model zdefiniowano klasy odwzorowujace tabele bazy danych. "
        "Klasa Projekt zawiera pola: projektId, nazwa, opis, dataCzasUtworzenia (LocalDateTime), "
        "dataOddania (LocalDate). Klasa Zadanie zawiera: zadanieId, nazwa, opis, kolejnosc, "
        "dataCzasUtworzenia, projektId (klucz obcy). Zastosowano konstruktory: bezparametrowy, "
        "z wszystkimi polami oraz z pominieciem ID. Gettery i settery wygenerowano automatycznie."
    )
    pdf.code_block("""\
public class Projekt {
    private Integer projektId;
    private String nazwa;
    private String opis;
    private LocalDateTime dataCzasUtworzenia;
    private LocalDate dataOddania;
    public Projekt() {}
    public Projekt(Integer projektId, String nazwa, String opis,
                   LocalDateTime dataCzasUtworzenia, LocalDate dataOddania) { ... }
    public Projekt(String nazwa, String opis,
                   LocalDateTime dataCzasUtworzenia, LocalDate dataOddania) { ... }
    // gettery i settery
}""")

    pdf.code_block("""\
public class Zadanie {
    private Integer zadanieId;
    private String nazwa;
    private String opis;
    private Integer kolejnosc;
    private LocalDateTime dataCzasUtworzenia;
    private Integer projektId;
    // konstruktory, gettery, settery
}""")

    # ===================== DATASOURCE =====================
    pdf.section_title("Pula polaczen - klasa DataSource (Singleton)")
    pdf.body_text(
        "Klasa DataSource implementuje wzorzec Singleton dla HikariDataSource. "
        "Konfiguruje URL do lokalnej bazy HSQLDB (tryb plikowy) z parametrami: "
        "hsqldb.write_delay=false (brak opoznienia zapisu) oraz sql.syntax_pgs=true "
        "(zgodnosc z PostgreSQL, wsparcie dla SERIAL). Rozmiar puli = 1."
    )
    pdf.code_block("""\
public class DataSource {
    private final static String DB_DIR = "db";
    private final static String DB_NAME = "projekty";
    private final static String DB_USERNAME = "admin";
    private final static String DB_USER_PASSWORD = "admin";
    private final static String HSQL_ADDITIONAL_PARAMS =
        ";hsqldb.write_delay=false;sql.syntax_pgs=true";
    private final static String DB_URL =
        String.format("jdbc:hsqldb:file:%s/%s%s", DB_DIR, DB_NAME, HSQL_ADDITIONAL_PARAMS);
    private final static HikariDataSource ds;

    static {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(DB_URL);
        config.setUsername(DB_USERNAME);
        config.setPassword(DB_USER_PASSWORD);
        config.setMaximumPoolSize(1);
        ds = new HikariDataSource(config);
    }
    private DataSource() {}
    public static Connection getConnection() throws SQLException {
        return ds.getConnection();
    }
}""")

    # ===================== DB INITIALIZER =====================
    pdf.section_title("Inicjalizacja bazy danych - DbInitializer")
    pdf.body_text(
        "Klasa DbInitializer tworzy strukture bazy podczas uruchamiania. "
        "Wykorzystuje transakcje: wylacza auto-commit, wykonuje zapytania, "
        "commit. W przypadku bledu - rollback. Tabele tworzone sa z opcja "
        "IF NOT EXISTS, klucz obcy z ON DELETE CASCADE."
    )
    pdf.code_block("""\
CREATE TABLE IF NOT EXISTS projekt (
    projekt_id SERIAL,
    nazwa VARCHAR(50) NOT NULL,
    opis VARCHAR(1000),
    dataczas_utworzenia TIMESTAMP DEFAULT now(),
    data_oddania DATE,
    CONSTRAINT projekt_pk PRIMARY KEY (projekt_id)
);
CREATE TABLE IF NOT EXISTS zadanie (
    zadanie_id SERIAL,
    nazwa VARCHAR(50) NOT NULL,
    opis VARCHAR(1000),
    kolejnosc INTEGER,
    dataczas_utworzenia TIMESTAMP DEFAULT now(),
    projekt_id INTEGER NOT NULL,
    CONSTRAINT zadanie_pk PRIMARY KEY (zadanie_id)
);
CREATE INDEX IF NOT EXISTS projekt_nazwa_idx ON projekt(nazwa);
CREATE INDEX IF NOT EXISTS zadanie_nazwa_idx ON zadanie(nazwa);
ALTER TABLE zadanie ADD CONSTRAINT IF NOT EXISTS zadanie_projekt_fk
    FOREIGN KEY (projekt_id) REFERENCES projekt (projekt_id) ON DELETE CASCADE;
ALTER TABLE zadanie ADD CONSTRAINT IF NOT EXISTS unique_kolejnosc UNIQUE (kolejnosc, projekt_id);""")

    # ===================== DAO =====================
    pdf.add_page()
    pdf.section_title("Warstwa DAO - interfejsy i implementacje")
    pdf.body_text(
        "Wzorzec DAO hermetyzuje dostep do danych. Interfejs ProjektDAO definiuje metody: "
        "getProjekt, setProjekt (INSERT/UPDATE), deleteProjekt, getProjekty (z paginacja "
        "LIMIT/OFFSET), getProjektyWhereNazwaLike, getProjektyWhereDataOddaniaIs oraz "
        "metody zliczajace wiersze. Implementacja uzywa PreparedStatement "
        "zapobiegajacego SQL Injection."
    )
    pdf.code_block("""\
public interface ProjektDAO {
    Projekt getProjekt(Integer projektId);
    void setProjekt(Projekt projekt);
    void deleteProjekt(Integer projektId);
    List<Projekt> getProjekty(Integer offset, Integer limit);
    List<Projekt> getProjektyWhereNazwaLike(String nazwa, Integer offset, Integer limit);
    List<Projekt> getProjektyWhereDataOddaniaIs(LocalDate d, Integer offset, Integer limit);
    int getRowsNumber();
    int getRowsNumberWhereNazwaLike(String nazwa);
    int getRowsNumberWhereDataOddaniaIs(LocalDate d);
}""")

    pdf.body_text("Implementacja metody setProjekt (INSERT/UPDATE z pobraniem klucza):")
    pdf.code_block("""\
@Override
public void setProjekt(Projekt p) {
    boolean insert = p.getProjektId() == null;
    String sql = insert ?
       "INSERT INTO projekt(nazwa,opis,dataczas_utworzenia,data_oddania) VALUES(?,?,?,?)"
       : "UPDATE projekt SET nazwa=?,opis=?,dataczas_utworzenia=?,data_oddania=?"
         + " WHERE projekt_id=?";
    try (Connection c = DataSource.getConnection();
         PreparedStatement ps = c.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
        ps.setString(1, p.getNazwa());
        ps.setString(2, p.getOpis());
        if (p.getDataCzasUtworzenia() == null)
            p.setDataCzasUtworzenia(LocalDateTime.now());
        ps.setObject(3, p.getDataCzasUtworzenia());
        ps.setObject(4, p.getDataOddania());
        if (!insert) ps.setInt(5, p.getProjektId());
        ps.executeUpdate();
        if (insert) {
            try (ResultSet rs = ps.getGeneratedKeys()) {
                if (rs.next()) p.setProjektId(rs.getInt(1));
            }
        }
    } catch (Exception e) {
        throw new RuntimeException(e);
    }
}""")

    pdf.body_text("Metoda getProjekty z paginacja (LIMIT/OFFSET):")
    pdf.code_block("""\
@Override
public List<Projekt> getProjekty(Integer offset, Integer limit) {
    List<Projekt> list = new ArrayList<>();
    try (Connection c = DataSource.getConnection();
         PreparedStatement ps = c.prepareStatement(
             "SELECT * FROM projekt ORDER BY dataczas_utworzenia DESC LIMIT ? OFFSET ?")) {
        ps.setInt(1, limit);   ps.setInt(2, offset);
        ResultSet rs = ps.executeQuery();
        while (rs.next()) {
            Projekt p = new Projekt();
            p.setProjektId(rs.getInt(1));
            p.setNazwa(rs.getString(2));
            p.setOpis(rs.getString(3));
            p.setDataCzasUtworzenia(rs.getObject(4, LocalDateTime.class));
            p.setDataOddania(rs.getObject(5, LocalDate.class));
            list.add(p);
        }
    } catch (Exception e) {
        throw new RuntimeException(e);
    }
    return list;
}""")

    pdf.body_text(
        "Analogicznie zaimplementowano interfejs ZadanieDAO i klase ZadanieDAOImpl "
        "obslugujace operacje CRUD dla tabeli 'zadanie'."
    )

    # ===================== INTERFEJS GRAFICZNY =====================
    pdf.add_page()
    pdf.section_title("Interfejs graficzny (JavaFX FXML)")
    pdf.body_text(
        "Interfejs uzytkownika zbudowano z wykorzystaniem plikow FXML. "
        "Glowne okno (ProjectFrame.fxml) zawiera: pole wyszukiwania, tabele z projektami, "
        "przyciski nawigacji (|◄ ◄ ► ►|) oraz ChoiceBox do wyboru rozmiaru strony. "
        "Okno zadan (ZadanieFrame.fxml) wyswietla liste zadan dla wybranego projektu."
    )
    pdf.code_block("""\
<!-- ProjectFrame.fxml - glowny interfejs -->
<BorderPane prefHeight="600" prefWidth="900"
    xmlns:fx="http://javafx.com/fxml/1"
    fx:controller="com.project.controller.ProjectController">
    <top>
        <HBox alignment="CENTER_LEFT" spacing="10">
            <Label text="Wyszukaj:" />
            <TextField fx:id="txtSzukaj" promptText="Nazwa, data lub ID..." />
            <Button onAction="#onActionBtnSzukaj" text="Szukaj" />
            <Region HBox.hgrow="ALWAYS" />
            <Button onAction="#onActionBtnDodaj" text="Dodaj projekt" />
        </HBox>
    </top>
    <center>
        <TableView fx:id="tblProjekt">
            <columns>
                <TableColumn fx:id="colId" text="ID" />
                <TableColumn fx:id="colNazwa" text="Nazwa" />
                <TableColumn fx:id="colOpis" text="Opis" />
                <TableColumn fx:id="colDataCzasUtworzenia" text="Utworzono" />
                <TableColumn fx:id="colDataOddania" text="Termin" />
            </columns>
        </TableView>
    </center>
    <bottom>
        <HBox alignment="CENTER" spacing="10">
            <Button fx:id="btnPierwsza" onAction="#onActionBtnPierwsza" text="|◄" />
            <Button fx:id="btnWstecz" onAction="#onActionBtnWstecz" text="◄" />
            <Label text="Rozmiar strony:" />
            <ChoiceBox fx:id="cbPageSizes" />
            <Button fx:id="btnDalej" onAction="#onActionBtnDalej" text="►" />
            <Button fx:id="btnOstatnia" onAction="#onActionBtnOstatnia" text="►|" />
        </HBox>
    </bottom>
</BorderPane>""")

    pdf.code_block("""\
<!-- ZadanieFrame.fxml - okno zadan -->
<BorderPane prefHeight="500" prefWidth="800"
    xmlns:fx="http://javafx.com/fxml/1"
    fx:controller="com.project.controller.ZadanieController">
    <top>
        <HBox alignment="CENTER_LEFT" spacing="10">
            <Label fx:id="lblTytul" text="Zadania dla projektu" />
            <Region HBox.hgrow="ALWAYS" />
            <Button onAction="#onActionBtnDodaj" text="Dodaj zadanie" />
        </HBox>
    </top>
    <center>
        <TableView fx:id="tblZadanie">
            <columns>
                <TableColumn fx:id="colId" text="ID" />
                <TableColumn fx:id="colNazwa" text="Nazwa" />
                <TableColumn fx:id="colOpis" text="Opis" />
                <TableColumn fx:id="colKolejnosc" text="Kolejnosc" />
                <TableColumn fx:id="colDataCzasUtworzenia" text="Utworzono" />
            </columns>
        </TableView>
    </center>
    <bottom>
        <Button fx:id="btnPowrot" onAction="#onActionBtnPowrot" text="Powrot" />
    </bottom>
</BorderPane>""")

    # ===================== KONTROLER =====================
    pdf.add_page()
    pdf.section_title("Warstwa kontrolera - ProjectController")
    pdf.body_text(
        "Klasa ProjectController zarzadza interfejsem uzytkownika i obsluga zdarzen. "
        "Zawiera komponenty GUI opatrzone adnotacja @FXML, zmienne do obslugi "
        "stronicowania (search4, pageNo, pageSize), ExecutorService (jednowatkowy) "
        "do asynchronicznego pobierania danych oraz ObservableList<Projekt>."
    )

    pdf.body_text("Inicjalizacja (metoda initialize):")
    pdf.code_block("""\
@FXML public void initialize() {
    search4 = "";  pageNo = 0;  pageSize = 10;
    cbPageSizes.getItems().addAll(5, 10, 20, 50, 100);
    cbPageSizes.setValue(pageSize);
    cbPageSizes.setOnAction(e -> {
        pageSize = cbPageSizes.getValue();
        pageNo = 0;
        wykonawca.execute(() -> loadPage(search4, pageNo, pageSize));
    });
    colId.setCellValueFactory(new PropertyValueFactory<>("projektId"));
    colNazwa.setCellValueFactory(new PropertyValueFactory<>("nazwa"));
    colOpis.setCellValueFactory(new PropertyValueFactory<>("opis"));
    colDataCzasUtworzenia.setCellValueFactory(
        new PropertyValueFactory<>("dataCzasUtworzenia"));
    colDataOddania.setCellValueFactory(new PropertyValueFactory<>("dataOddania"));
    // Formatowanie daty
    colDataCzasUtworzenia.setCellFactory(column -> new TableCell<>() {
        @Override
        protected void updateItem(LocalDateTime item, boolean empty) {
            super.updateItem(item, empty);
            setText(empty || item == null ? null : dateTimeFormatter.format(item));
        }
    });
    projekty = FXCollections.observableArrayList();
    tblProjekt.setItems(projekty);
    // Kolumna z przyciskami
    wykonawca.execute(() -> loadPage(search4, pageNo, pageSize));
}""")

    pdf.body_text("Wczytywanie danych z paginacja i wyszukiwaniem (wyrazenia regularne):")
    pdf.code_block("""\
private void loadPage(String search4, Integer pageNo, Integer pageSize) {
    try {
        List<Projekt> lista = new ArrayList<>();
        if (search4 != null && !search4.isEmpty()) {
            if (search4.matches("[0-9]+")) {
                // Szukaj po ID
                Projekt p = projektDAO.getProjekt(Integer.parseInt(search4));
                if (p != null) lista.add(p);
            } else if (search4.matches("^\\\\d{4}-\\\\d{2}-\\\\d{2}$")) {
                // Szukaj po dacie oddania
                lista.addAll(projektDAO.getProjektyWhereDataOddaniaIs(
                    LocalDate.parse(search4), pageNo * pageSize, pageSize));
            } else {
                // Szukaj po nazwie (LIKE)
                lista.addAll(projektDAO.getProjektyWhereNazwaLike(
                    search4, pageNo * pageSize, pageSize));
            }
        } else {
            lista.addAll(projektDAO.getProjekty(pageNo * pageSize, pageSize));
        }
        Platform.runLater(() -> {
            projekty.clear();
            projekty.addAll(lista);
        });
    } catch (Exception e) {
        logger.error("Blad ladowania danych", e);
    }
}""")

    pdf.body_text("Obsluga przyciskow nawigacji:")
    pdf.code_block("""\
@FXML private void onActionBtnSzukaj(ActionEvent e) {
    search4 = txtSzukaj.getText();  pageNo = 0;
    wykonawca.execute(() -> loadPage(search4, pageNo, pageSize));
}
@FXML private void onActionBtnDalej(ActionEvent e) {
    pageNo++;
    wykonawca.execute(() -> loadPage(search4, pageNo, pageSize));
}
@FXML private void onActionBtnWstecz(ActionEvent e) {
    if (pageNo > 0) pageNo--;
    wykonawca.execute(() -> loadPage(search4, pageNo, pageSize));
}
@FXML private void onActionBtnPierwsza(ActionEvent e)  { pageNo = 0;  ... }
@FXML private void onActionBtnOstatnia(ActionEvent e)   { pageNo = 9999; ... }""")

    pdf.body_text("Kolumna z przyciskami (Edycja, Usun, Zadania):")
    pdf.code_block("""\
TableColumn<Projekt, Void> colEdit = new TableColumn<>("Edycja");
colEdit.setCellFactory(column -> new TableCell<>() {
    private final GridPane pane;
    {
        Button btnTask = new Button("Zadania");
        Button btnEdit = new Button("Edycja");
        Button btnRemove = new Button("Usun");
        btnTask.setOnAction(e -> openZadanieFrame(getCurrentProjekt()));
        btnEdit.setOnAction(e -> edytujProjekt(getCurrentProjekt()));
        btnRemove.setOnAction(e -> usunProjekt(getCurrentProjekt()));
        pane = new GridPane();
        pane.add(btnTask, 0, 0);
        pane.add(btnEdit, 0, 1);
        pane.add(btnRemove, 0, 2);
    }
    private Projekt getCurrentProjekt() {
        return getTableView().getItems().get(getIndex());
    }
    @Override protected void updateItem(Void item, boolean empty) {
        setGraphic(empty ? null : pane);
    }
});
tblProjekt.getColumns().add(colEdit);""")

    pdf.body_text("Dialog dodawania/edycji projektu:")
    pdf.code_block("""\
private void edytujProjekt(Projekt projekt) {
    Dialog<Projekt> dialog = new Dialog<>();
    dialog.setTitle("Edycja");
    TextField txtNazwa = new TextField(projekt.getNazwa());
    TextArea txtOpis = new TextArea(projekt.getOpis());
    DatePicker datePicker = new DatePicker(projekt.getDataOddania());
    GridPane grid = new GridPane();
    grid.add(new Label("Nazwa:"), 0, 0);  grid.add(txtNazwa, 1, 0);
    grid.add(new Label("Opis:"), 0, 1);   grid.add(txtOpis, 1, 1);
    grid.add(new Label("Data oddania:"), 0, 2);  grid.add(datePicker, 1, 2);
    dialog.getDialogPane().setContent(grid);
    ButtonType ok = new ButtonType("Zapisz", ButtonBar.ButtonData.OK_DONE);
    dialog.getDialogPane().getButtonTypes().addAll(ok, ButtonType.CANCEL);
    dialog.setResultConverter(btn -> {
        if (btn == ok) {
            projekt.setNazwa(txtNazwa.getText());
            projekt.setOpis(txtOpis.getText());
            projekt.setDataOddania(datePicker.getValue());
            return projekt;
        }
        return null;
    });
    Optional<Projekt> result = dialog.showAndWait();
    result.ifPresent(p -> wykonawca.execute(() -> {
        projektDAO.setProjekt(p);
        Platform.runLater(() -> {
            if (!projekty.contains(p)) projekty.add(0, p);
            tblProjekt.refresh();
        });
    }));
}""")

    pdf.body_text("Usuwanie projektu z potwierdzeniem i shutdown puli watkow:")
    pdf.code_block("""\
private void usunProjekt(Projekt projekt) {
    Alert alert = new Alert(AlertType.CONFIRMATION);
    alert.setHeaderText("Usunac projekt?");
    alert.setContentText(projekt.getNazwa());
    Optional<ButtonType> result = alert.showAndWait();
    if (result.isPresent() && result.get() == ButtonType.OK) {
        wykonawca.execute(() -> {
            projektDAO.deleteProjekt(projekt.getProjektId());
            Platform.runLater(() -> projekty.remove(projekt));
        });
    }
}
public void shutdown() {
    if (wykonawca != null) {
        wykonawca.shutdown();
        try {
            if (!wykonawca.awaitTermination(5, TimeUnit.SECONDS))
                wykonawca.shutdownNow();
        } catch (InterruptedException e) {
            wykonawca.shutdownNow();
        }
    }
}""")

    # ===================== ZADANIE CONTROLLER =====================
    pdf.add_page()
    pdf.section_title("Kontroler zadan - ZadanieController")
    pdf.body_text(
        "Klasa obsluguje okno zadan przypisanych do projektu. W konstruktorze przyjmuje "
        "obiekt Projekt, ZadanieDAO oraz ExecutorService. Metoda loadZadania() pobiera "
        "zadania z bazy. Zaimplementowano pelny CRUD: dodawanie, edycje oraz usuwanie "
        "z potwierdzeniem. Przycisk Powrot zamyka okno poprzez WindowEvent."
    )
    pdf.code_block("""\
public class ZadanieController {
    private final Projekt projekt;
    private final ZadanieDAO zadanieDAO;
    private final ExecutorService wykonawca;
    @FXML private Button btnPowrot;
    @FXML private Label lblTytul;
    @FXML private TableView<Zadanie> tblZadanie;
    // kolumny: colId, colNazwa, colOpis, colKolejnosc, colDataCzasUtworzenia

    public ZadanieController(Projekt projekt, ZadanieDAO zadanieDAO,
                             ExecutorService wykonawca) {
        this.projekt = projekt;
        this.zadanieDAO = zadanieDAO;
        this.wykonawca = wykonawca;
    }

    @FXML public void initialize() {
        lblTytul.setText("Zadania dla projektu: " + projekt.getNazwa());
        // inicjalizacja kolumn, dodanie kolumny akcji
        wykonawca.execute(this::loadZadania);
    }

    private void loadZadania() {
        List<Zadanie> lista = zadanieDAO.getZadania(projekt.getProjektId());
        Platform.runLater(() -> { zadania.clear();  zadania.addAll(lista); });
    }

    @FXML private void onActionBtnPowrot(ActionEvent event) {
        Stage stage = (Stage) btnPowrot.getScene().getWindow();
        stage.fireEvent(new WindowEvent(stage, WindowEvent.WINDOW_CLOSE_REQUEST));
    }

    @FXML private void onActionBtnDodaj(ActionEvent event) {
        Zadanie z = new Zadanie();
        z.setProjektId(projekt.getProjektId());
        edytujZadanie(z);
    }
    // edytujZadanie, usunZadanie - analogicznie jak ProjectController
}""")

    # ===================== KLASA URUCHOMIENIOWA =====================
    pdf.section_title("Klasa uruchomieniowa - ProjectClientApplication")
    pdf.body_text(
        "Klasa rozszerza javafx.application.Application. W main() wywolywany jest "
        "DbInitializer.init() a nastepnie launch(). W start() ladowany jest FXML, "
        "tworzony ProjektDAOImpl i przekazywany do kontrolera przez setControllerFactory. "
        "Rejestrowana jest obsluga zamkniecia okna: shutdown() + Platform.exit()."
    )
    pdf.code_block("""\
public class ProjectClientApplication extends Application {
    @Override
    public void start(Stage stage) throws Exception {
        FXMLLoader loader = new FXMLLoader(
            getClass().getResource("/fxml/ProjectFrame.fxml"));
        ProjektDAO dao = new ProjektDAOImpl();
        loader.setControllerFactory(c -> new ProjectController(dao));
        Scene scene = new Scene(loader.load());
        scene.getStylesheets().add(
            getClass().getResource("/css/application.css").toExternalForm());
        ProjectController controller = loader.getController();
        stage.setOnCloseRequest(e -> { controller.shutdown(); Platform.exit(); });
        stage.setTitle("Projekty");
        stage.setScene(scene);
        stage.show();
    }
    public static void main(String[] args) {
        DbInitializer.init();
        launch(args);
    }
}""")

    # ===================== MODULE-INFO =====================
    pdf.section_title("Modul Java - module-info.java")
    pdf.code_block("""\
module project.jfx.client {
    exports com.project.datasource;
    exports com.project.dao;
    exports com.project.model;
    exports com.project.app;
    exports com.project.controller;
    requires javafx.base;
    requires javafx.fxml;
    requires javafx.controls;
    requires transitive javafx.graphics;
    requires com.zaxxer.hikari;
    requires transitive java.sql;
    requires org.hsqldb;
    requires org.slf4j;
    requires ch.qos.logback.classic;
    requires ch.qos.logback.core;
    opens com.project.app to javafx.graphics, javafx.fxml, javafx.base, javafx.controls;
    opens com.project.model to javafx.graphics, javafx.fxml, javafx.base, javafx.controls;
    opens com.project.controller to javafx.graphics, javafx.fxml, javafx.base, javafx.controls;
}""")

    # ===================== ODPOWIEDZI =====================
    pdf.add_page()
    pdf.section_title("Opis problemu do rozwiazania - odpowiedzi na pytania")

    qa = [
        ("Jakie biblioteki zostaly uzyte?",
         "HSQLDB 2.7.4 (baza danych), HikariCP 6.2.1 (pula polaczen), "
         "Logback 1.5.17 + SLF4J 2.0.17 (logowanie), JavaFX 23.0.2 (GUI)."),
        ("Do czego sluzy plik build.gradle?",
         "Jest plikiem konfiguracyjnym Gradle. Okresla zaleznosci, wersje, wtyczki, "
         "kodowanie, klase glowna i modul. Umożliwia zbudowanie i uruchomienie "
         "projektu jednym poleceniem."),
        ("Co to jest HikariCP i dlaczego go uzywamy?",
         "HikariCP to lekka biblioteka do zarzadzania pula polaczen. Zamiast tworzyc "
         "nowe polaczenie za kazdym razem, pula przechowuje gotowe polaczenia, "
         "co znaczaco poprawia wydajnosc. W aplikacji max. rozmiar puli = 1."),
        ("Czym jest wzorzec Singleton w klasie DataSource?",
         "Singleton ogranicza mozliwosc utworzenia tylko jednej instancji. "
         "Prywatny konstruktor (private DataSource()) uniemozliwia tworzenie "
         "instancji, a statyczny blok inicjalizujacy tworzy pojedynczy HikariDataSource."),
        ("Dlaczego uzywamy PreparedStatement zamiast Statement?",
         "PreparedStatement zapobiega SQL Injection poprzez automatyczne escapowanie "
         "parametrow. Ponadto pozwala na prekompilacje zapytania, co poprawia "
         "wydajnosc przy wielokrotnym wykonywaniu tego samego zapytania."),
        ("Jak dziala transakcja w DbInitializer?",
         "Metoda init() wylacza auto-commit, wykonuje wszystkie zapytania, po czym "
         "wywoluje commit(). Przy bledzie - rollback(). Dzieki temu operacje sa "
         "atomowe: wszystkie albo zadna."),
        ("Jak dziala stronicowanie w aplikacji?",
         "Zrealizowano przez OFFSET i LIMIT w SQL. pageNo * pageSize = OFFSET, "
         "pageSize = LIMIT. Przyciski nawigacji modyfikuja pageNo. ChoiceBox "
         "pozwala zmienic pageSize (5, 10, 20, 50, 100)."),
        ("Jak dziala wyszukiwanie?",
         "Wykorzystuje wyrazenia regularne: cyfry -> szukaj po ID; "
         "wzorzec RRRR-MM-DD -> szukaj po dacie oddania; "
         "w pozostalych przypadkach -> szukaj po nazwie (LIKE '%fraza%')."),
        ("Jak dziala kolumna 'Edycja' z przyciskami?",
         "Dodatkowa TableColumn z niestandardowa CellFactory. Kazda komorka "
         "zawiera GridPane z 3 przyciskami: Zadania (otwiera okno zadan), "
         "Edycja (otwiera dialog edycji), Usun (usuwa po potwierdzeniu)."),
        ("Do czego sluzy ExecutorService?",
         "ExecutorService zarzadza pula watkow. Jednowatkowa pula (newFixedThreadPool(1)) "
         "wykonuje zadania w tle, nie blokujac watku JavaFX Application Thread. "
         "Metoda shutdown() zapewnia grzeczne zakonczenie watkow przy zamknieciu."),
    ]

    for q, a in qa:
        pdf.set_font("TNR", "B", 12)
        pdf.cell(0, 6, q, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("TNR", "", 12)
        pdf.multi_cell(0, 5.5, a)
        pdf.ln(3)

    # ===================== WNIOSKI =====================
    pdf.add_page()
    pdf.section_title("Wnioski")
    pdf.body_text(
        "Realizacja zadania pozwolila na praktyczne zapoznanie sie z budowa aplikacji "
        "bazodanowej w jezyku Java z wykorzystaniem nowoczesnych bibliotek i wzorcow "
        "projektowych. W szczegolnosci:"
    )
    bullets = [
        "Stosowanie JDBC z PreparedStatement zapewnia bezpieczenstwo i wydajnosc zapytan.",
        "HikariCP jako pula polaczen eliminuje narzut zwiazany z tworzeniem nowych polaczen.",
        "Wzorzec DAO hermetyzuje logike dostepu do danych, ulatwiajac testowanie i modyfikacje.",
        "JavaFX z FXML i Scene Builder umozliwia szybkie projektowanie interfejsu uzytkownika.",
        "ExecutorService pozwala na asynchroniczne ladowanie danych bez blokowania GUI.",
        "ObservableList zapewnia automatyczna synchronizacje danych z widokiem tabeli.",
        "Mechanizm logowania (Logback) ulatwia diagnozowanie bledow w aplikacji.",
        "Wyrazenia regularne pozwalaja na elastyczne wyszukiwanie (ID, data, nazwa).",
        "Transakcje bazodanowe gwarantuja spojnosc danych przy tworzeniu struktury BD.",
        "System budowania Gradle upraszcza zarzadzanie zaleznosciami i budowanie projektu.",
    ]
    for b in bullets:
        pdf.set_font("TNR", "", 12)
        pdf.cell(5, 5.5, "-")
        pdf.multi_cell(0, 5.5, b)
        pdf.ln(1)

    pdf.ln(5)
    pdf.set_font("TNR", "I", 12)
    pdf.cell(0, 7, "Repozytorium: https://github.com/Gaz3ll/Zaawansowane_Programowanie_Obiektowe", new_x="LMARGIN", new_y="NEXT")

    # Save
    out = "D:/eclipse-2024-09/workspace/project-jfx-client/sprawozdanie.pdf"
    pdf.output(out)
    print(f"PDF saved: {out}")


if __name__ == "__main__":
    build_report()
