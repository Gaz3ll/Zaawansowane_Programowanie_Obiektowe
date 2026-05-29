from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import datetime

doc = Document()

style = doc.styles['Normal']
font = style.font
font.name = 'Consolas'
font.size = Pt(10)
style.paragraph_format.space_after = Pt(4)
style.paragraph_format.line_spacing = 1.15

# ===== TITLE =====
for _ in range(3):
    doc.add_paragraph()

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run('Sprawozdanie')
run.font.size = Pt(28)
run.bold = True
run.font.name = 'Calibri'

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run('Integracja project-rest-api oraz project-web-app\nw jeden projekt Spring Boot')
run.font.size = Pt(14)
run.font.color.rgb = RGBColor(0x22, 0x55, 0xAA)
run.font.name = 'Calibri'

doc.add_paragraph()
d = doc.add_paragraph()
d.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = d.add_run(f'Data: {datetime.date.today().strftime("%d.%m.%Y")}')
run.font.size = Pt(12)
run.font.name = 'Calibri'

doc.add_page_break()

# ===== Helper =====
def code(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5)
    run = p.add_run(text)
    run.font.size = Pt(9)
    run.font.name = 'Consolas'
    return p

def bullet(text):
    doc.add_paragraph(text, style='List Bullet')

# ===== 1. CEL =====
doc.add_heading('1. Cel zadania', level=1)
doc.add_paragraph(
    'Scalenie dwoch niezaleznych projektow:\n'
    '  - project-rest-api  (REST API + JPA + PostgreSQL)\n'
    '  - project-web-app   (Thymeleaf UI komunikujacy sie z API przez HTTP)\n'
    'w jeden projekt uruchamiany pojedynczym poleceniem, bez utraty funkcjonalnosci.'
)

# ===== 2. STRUKTURA PROJEKTU =====
doc.add_heading('2. Struktura projektu', level=1)

doc.add_heading('2.1. Katalogi zrodlowe', level=2)
code('''project-integrated/
  build.gradle
  settings.gradle
  src/main/java/com/project/
    ProjectIntegratedApplication.java
    config/
      JpaConfig.java              @EnableJpaAuditing
      SecurityConfig.java         FilterChain z BasicAuth
    model/
      Projekt.java                @Entity, @CreatedDate, @LastModifiedDate
      Student.java                @Entity
      Zadanie.java                @Entity, @ManyToOne -> Projekt
    repository/
      ProjektRepository.java      JpaRepository + findByNazwaContainingIgnoreCase
      StudentRepository.java      JpaRepository + findByNazwiskoStartsWithIgnoreCase
      ZadanieRepository.java      JpaRepository + @Query findZadaniaProjektu
    service/
      ProjektService.java         interfejs
      ProjektServiceImpl.java     JPA-based impl
      StudentService.java         interfejs
      StudentServiceImpl.java     JPA-based impl
      ZadanieService.java         interfejs
      ZadanieServiceImpl.java     JPA-based impl
    controller/
      api/
        ProjektRestController.java   GET/POST/PUT/DELETE /api/projekty
        StudentRestController.java   GET/POST/PUT/DELETE /api/studenci
        ZadanieRestController.java   GET/POST/PUT/DELETE /api/zadania
      web/
        HomeController.java          GET / -> redirect:/projektList
        ProjectController.java       GET/POST /projektList, /projektEdit
        StudentController.java       GET/POST /studentList, /studentEdit
        ZadanieController.java       GET/POST /zadanieList, /zadanieEdit
    exception/
      HttpException.java
  src/main/resources/
    application.properties
    logback-spring.xml
    templates/
      projektList.html, projektEdit.html
      studentList.html, studentEdit.html
      zadanieList.html, zadanieEdit.html
    static/css/
      list-style.css
      edit-style.css''')

doc.add_heading('2.2. Build.gradle (zaleznosci)', level=2)
code('''plugins {
    id 'java'
    id 'org.springframework.boot' version '3.4.3'
    id 'io.spring.dependency-management' version '1.1.7'
}
java { toolchain { languageVersion = JavaLanguageVersion.of(17) } }
repositories { mavenCentral() }

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
    implementation 'org.springframework.boot:spring-boot-starter-security'
    implementation 'org.springframework.boot:spring-boot-starter-thymeleaf'
    implementation 'org.springframework.boot:spring-boot-starter-validation'
    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'org.springframework.data:spring-data-commons'
    implementation 'com.fasterxml.jackson.datatype:jackson-datatype-jsr310'
    implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:2.7.0'
    developmentOnly 'org.springframework.boot:spring-boot-devtools'
    runtimeOnly 'org.postgresql:postgresql'
    compileOnly 'org.projectlombok:lombok'
    annotationProcessor 'org.projectlombok:lombok'
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
}''')

doc.add_heading('2.3. application.properties', level=2)
code('''spring.datasource.url=jdbc:postgresql://localhost:5432/projekty
spring.datasource.username=postgres
spring.datasource.password=postgres
spring.datasource.driver-class-name=org.postgresql.Driver
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
spring.security.user.name=admin
spring.security.user.password=admin
spring.threads.virtual.enabled=true
server.port=8080''')

# ===== 3. SZCZEGOLY TECHNICZNE =====
doc.add_heading('3. Szczegoly techniczne integracji', level=1)

doc.add_heading('3.1. Encje JPA (model)', level=2)
doc.add_paragraph(
    'Encje przejete z project-rest-api z adnotacjami JPA. Kluczowe wiazania:'
)
bullet('Projekt @OneToMany -> Zadanie, @ManyToMany -> Student (przez projekt_student)')
bullet('Student @ManyToMany(mappedBy="studenci") -> Projekt')
bullet('Zadanie @ManyToOne -> Projekt (klucz obcy projekt_id)')
bullet('@CreatedDate / @LastModifiedDate dzieki @EnableJpaAuditing w JpaConfig')
bullet('Walidacja: @NotBlank, @Size na polach, obslugiwana przez @Valid w kontrolerach')

doc.add_heading('3.2. Warstwa serwisowa', level=2)
doc.add_paragraph(
    'Serwisy JPA (ProjektServiceImpl, StudentServiceImpl, ZadanieServiceImpl) '
    'sa wspoldzielone miedzy kontrolerami REST a web. Kazdy serwis:'
)
bullet('Przyjmuje repozytorium JPA przez konstruktor (Dependency Injection)')
bullet('Operacje CRUD: findById, save, deleteById')
bullet('Metody wyszukiwania: findByNazwaContainingIgnoreCase, findByNazwiskoStartsWithIgnoreCase')
bullet('Kaskadowe usuwanie: ProjektServiceImpl.deleteProjekt usuwa najpierw powiazane Zadania')
bullet('Stronicowanie: wszystkie metody get/list przyjmuja Pageable i zwracaja Page<T>')

doc.add_heading('3.3. REST API (/api/...)', level=2)
doc.add_paragraph(
    'Trzy kontrolery REST (ProjektRestController, StudentRestController, ZadanieRestController) '
    'udostepniaja pelny CRUD:'
)
code('''GET    /api/projekty                   -> Page<Projekt>
GET    /api/projekty?nazwa=...       -> Page<Projekt> (filtrowanie)
GET    /api/projekty/{id}            -> ResponseEntity<Projekt>
POST   /api/projekty                 -> 201 Created + Location header
PUT    /api/projekty/{id}            -> 200 OK lub 404
DELETE /api/projekty/{id}            -> 200 OK lub 404
(pelny analog dla /api/studenci i /api/zadania)''')
doc.add_paragraph(
    'Obsluga bledow: ResponseEntity.of() dla 404, @Valid + MethodArgumentNotValidException '
    'dla 400, ServletUriComponentsBuilder dla Location header przy POST.'
)

doc.add_heading('3.4. Web UI (Thymeleaf)', level=2)
doc.add_paragraph(
    'Kontrolery MVC (ProjectController, StudentController, ZadanieController) obsluguja '
    'strony HTML z szablonow Thymeleaf. Roznica wzgledem oryginalnego project-web-app:'
)
bullet('Zamiast RestClient -> bezposrednio serwisy JPA (ProjektService, StudentService, ZadanieService)')
bullet('Brak klas RestResponsePage, ServiceUtil (niepotrzebne przy lokalnym wywolaniu)')
bullet('Brak lapania HttpException (serwisy JPA nie rzucaja tego wyjatku)')
bullet('Walidacja: @ModelAttribute @Valid + BindingResult, bledy wyswietlane w szablonie')
bullet('Przyciski: create/update/delete/cancel obslugiwane przez parametry POST (params="delete", params="cancel")')

doc.add_paragraph('Szablony Thymeleaf wykorzystuja:')
bullet('th:each do iteracji po listach (projekty, studenci, zadania)')
bullet('#temporals.format() do formatowania LocalDateTime / LocalDate')
bullet('th:field, th:errors do bindingu pol formularza i komunikatow bledow')
bullet('Operacje delete realizowane przez parametr GET ?delete=true + warunek w szablonie')

doc.add_heading('3.5. Konfiguracja Security', level=2)
code('''@Configuration
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/**").authenticated()
                .anyRequest().permitAll()
            )
            .httpBasic(Customizer.withDefaults())
            .build();
    }
}''')
doc.add_paragraph(
    'Endpointy /api/* wymagaja Basic Auth (domyslnie admin/admin z application.properties). '
    'Wszystkie inne sciezki (strony, CSS, Swagger) sa publiczne.'
)

doc.add_heading('3.6. Swagger UI', level=2)
doc.add_paragraph(
    'SpringDoc OpenAPI 2.7.0 udostepnia Swagger UI pod /swagger-ui.html '
    'oraz dokumentacje JSON pod /v3/api-docs. Kazdy REST kontroler ma adnotacje '
    '@Tag(name="Projekt"/"Student"/"Zadanie") dla czytelnego podzialu w UI.'
)

# ===== 4. NAJWIĘKSZA TRUDNOŚĆ =====
doc.add_heading('4. Najwieksza trudnosc — konflikt wersji springdoc', level=1)

doc.add_heading('4.1. Symptomy', level=2)
doc.add_paragraph(
    'Po uruchomieniu gradlew bootRun aplikacja crashowala z bledem:'
)
code('''java.lang.NoClassDefFoundError:
  org/springframework/boot/web/context/servlet/ApplicationServletEnvironment
Caused by: java.lang.ClassNotFoundException:
  org.springframework.boot.web.context.servlet.ApplicationServletEnvironment''')
doc.add_paragraph(
    'Klasa ApplicationServletEnvironment istniala w Spring Boot 2.x, ale zostala usunieta '
    'w Spring Boot 3.x (zrefactorowana do WebApplicationContext).'
)

doc.add_heading('4.2. Analiza drzewa zaleznosci', level=2)
doc.add_paragraph(
    'Uruchomienie gradlew dependencies --configuration runtimeClasspath '
    'ujawnilo zrodlo problemu:'
)
code('''org.springdoc:springdoc-openapi-starter-webmvc-ui:3.0.2
  +--- org.springframework.boot:spring-boot-starter:4.0.3 -> 3.4.3
  +--- org.springframework.boot:spring-boot-validation:4.0.3
  |    +--- org.springframework.boot:spring-boot:4.0.3 -> 3.4.3
  +--- org.springframework.boot:spring-boot-jackson:4.0.3
  +--- org.springframework.boot:spring-boot-webmvc:4.0.3
  |    +--- org.springframework.boot:spring-boot-http-converter:4.0.3
  |    +--- org.springframework.boot:spring-boot-servlet:4.0.3
  |    +--- org.springframework:spring-web:7.0.5 -> 6.2.3
  |    \--- org.springframework:spring-webmvc:7.0.5 -> 6.2.3
  \--- org.springframework.boot:spring-boot-web-server:4.0.3''')
doc.add_paragraph(
    'SpringDoc 3.0.2 zawiera zależności od artefaktów z grupy org.springframework.boot '
    'w wersji 4.0.3 (spring-boot-webmvc, spring-boot-web-server, spring-boot-validation, '
    'spring-boot-jackson). Nie są to standardowe moduły Spring Boot — to osobne biblioteki '
    'powstałe prawdopodobnie jako proof-of-concept lub wczesna wersja rozwojowa Spring Boot 4.x. '
    'Odwołują się one do klas, które nie istnieją w żadnej stabilnej wersji Spring Boot 3.x.'
)

doc.add_heading('4.3. Próby rozwiazania', level=2)
doc.add_paragraph('Próba 1 — wykluczenie zależności przejściowych (exclude):')
code('''implementation('org.springdoc:springdoc-openapi-starter-webmvc-ui:3.0.2') {
    exclude group: 'org.springframework.boot', module: 'spring-boot-webmvc'
    exclude group: 'org.springframework.boot', module: 'spring-boot-web-server'
    exclude group: 'org.springframework.boot', module: 'spring-boot-validation'
    exclude group: 'org.springframework.boot', module: 'spring-boot-jackson'
    exclude group: 'org.springframework.boot', module: 'spring-boot-http-converter'
    exclude group: 'org.springframework.boot', module: 'spring-boot-servlet'
}''')
doc.add_paragraph(
    'Rozwiazało to blad ApplicationServletEnvironment, ale ujawnilo kolejny: '
    'NoClassDefFoundError: org/springframework/web/accept/ApiVersionStrategy — '
    'kolejna klasa spoza standardowego Spring Boot 3.x, na ktorej polega SpringDoc 3.0.2.'
)

doc.add_paragraph('Próba 2 — zmiana wersji springdoc:')
code('''// Zamiast 3.0.2 (Spring Boot 4.x pre-release)
implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:2.7.0'  // Spring Boot 3.x''')
doc.add_paragraph(
    'SpringDoc stosuje konwencję: 1.x = Spring Boot 2.x, 2.x = Spring Boot 3.x, '
    '3.x = Spring Boot 4.x (pre-release). Wersja 2.7.0 jest w pełni kompatybilna '
    'ze Spring Boot 3.4.3 i nie ciągnie żadnych zależności spoza standardowego ekosystemu. '
    'Po zmianie aplikacja uruchomiła się poprawnie, a Swagger UI działa bez zastrzeżeń.'
)

doc.add_heading('4.4. Wnioski', level=2)
doc.add_paragraph(
    'Problemu nie dało się rozwiązać przez samo wykluczanie przejściowych zależności, '
    'ponieważ SpringDoc 3.0.2 został zbudowany tak, by wykorzystywać klasy z nowszych wersji Spring. '
    'Kluczowym wnioskiem jest konieczność weryfikacji kompatybilności wersji bibliotek '
    '(zwłaszcza tych oznaczonych jako "starter"). Narzędzie gradlew dependencies okazało się '
    'niezbędne do identyfikacji źródła problemu — bez analizy drzewa zależności przyczyna '
    '(artefakty 4.0.3 spoza standardowego Spring Boot) pozostałaby niewidoczna.'
)

# ===== 5. SCHEMAT DZIALANIA =====
doc.add_heading('5. Schemat dzialania aplikacji', level=1)
doc.add_paragraph('Przepływ danych dla operacji "Lista projektow" (web UI):')
code('''Przegladarka                    Serwer (8080)
    |                              |
    |--- GET /projektList -------->|
    |                              | ProjectController
    |                              |   -> ProjektService.getProjekty(Pageable)
    |                              |       -> ProjektRepository.findAll(Pageable)
    |                              |           -> PostgreSQL (SELECT ... LIMIT ...)
    |                              |   <- Page<Projekt>
    |                              |   -> thymeleaf renders projektList.html
    |<-- HTML (projektList) -------|
    |                              |
    |--- GET /api/projekty (auth)->|
    |                              | ProjektRestController
    |                              |   -> ProjektService.getProjekty(Pageable)
    |                              |       -> ProjektRepository.findAll(Pageable)
    |                              |   <- JSON: Page<Projekt>
    |<-- JSON ---------------------|''')

doc.add_paragraph('W porownaniu z oryginalnym rozwiazaniem (dwa procesy):')
code('''PRZED (dwa procesy):                    PO (jeden proces):
                                          
web-app (8081)  rest-api (8080)          integrated (8080)
  Controller       Controller               Controller
    |                 |                       |
    v                 |                       v
  RestClient -HTTP->  |                 Serwis JPA
    |                 v                       |
    v           Serwis JPA                    v
  ResponseEntity     |                 Repozytorium
    |                 v                       |
    v           Repozytorium                  v
  Thymeleaf          |                  PostgreSQL
    |                 v
    v           PostgreSQL''')

# ===== 6. URUCHOMIENIE =====
doc.add_heading('6. Uruchomienie', level=1)
code('''# Wymagania: Java 17+, PostgreSQL na localhost:5432 z baza "projekty"
cd project-integrated
.\\gradlew.bat bootRun''')
doc.add_paragraph('Dostepne endpointy po starcie:')
bullet('http://localhost:8080/ — przekierowanie do listy projektow')
bullet('http://localhost:8080/projektList — lista projektow')
bullet('http://localhost:8080/studentList — lista studentow')
bullet('http://localhost:8080/zadanieList — lista zadan')
bullet('http://localhost:8080/swagger-ui.html — Swagger UI')
bullet('http://localhost:8080/api/projekty — REST API (Basic Auth admin/admin)')

# ===== 7. PODSUMOWANIE =====
doc.add_heading('7. Podsumowanie', level=1)
doc.add_paragraph(
    'Projekt project-integrated stanowi w pelni funkcjonalne polaczenie dwoch poprzednich '
    'aplikacji w jeden proces Spring Boot 3.4.3. Oryginalne REST API dziala bez zmian pod '
    '/api/..., a interfejs uzytkownika Thymeleaf jest dostepny pod standardowymi sciezkami. '
    'Web kontrolery korzystaja teraz bezposrednio z serwisow JPA, co eliminuje narzut '
    'sieciowy, upraszcza kod (brak RestClient, RestResponsePage, ServiceUtil) i ulatwia '
    'utrzymanie. Konflikt wersji springdoc zostal rozwiazany przez wybor odpowiedniej galezi '
    'wersji (2.x zamiast 3.x) kompatybilnej ze Spring Boot 3.4.3.'
)

doc.save('Sprawozdanie_Integracja_REST_API_i_Web_UI.docx')
print("OK")
