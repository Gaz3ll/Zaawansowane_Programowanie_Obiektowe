package com.project.controller;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.project.dao.ProjektDAO;
import com.project.dao.ZadanieDAO;
import com.project.model.Projekt;

import javafx.application.Platform;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.*;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.layout.GridPane;
import javafx.util.Callback;
import javafx.util.StringConverter;

public class ProjectController {

   private static final Logger logger = LoggerFactory.getLogger(ProjectController.class);

   private String search4;
   private Integer pageNo;
   private Integer pageSize;

   private ObservableList<Projekt> projekty;

   private ExecutorService wykonawca;
   private ProjektDAO projektDAO;

   private static final DateTimeFormatter dateFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
   private static final DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

   // ===== GUI =====
   @FXML private ChoiceBox<Integer> cbPageSizes;
   @FXML private TableView<Projekt> tblProjekt;
   @FXML private TableColumn<Projekt, Integer> colId;
   @FXML private TableColumn<Projekt, String> colNazwa;
   @FXML private TableColumn<Projekt, String> colOpis;
   @FXML private TableColumn<Projekt, LocalDateTime> colDataCzasUtworzenia;
   @FXML private TableColumn<Projekt, LocalDate> colDataOddania;
   @FXML private TextField txtSzukaj;
   @FXML private Button btnDalej;
   @FXML private Button btnWstecz;
   @FXML private Button btnPierwsza;
   @FXML private Button btnOstatnia;

   public ProjectController(ProjektDAO projektDAO) {
      this.projektDAO = projektDAO;
      wykonawca = Executors.newFixedThreadPool(1);
   }

   @FXML
   public void initialize() {

      search4 = "";
      pageNo = 0;
      pageSize = 10;

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
      colDataCzasUtworzenia.setCellValueFactory(new PropertyValueFactory<>("dataCzasUtworzenia"));
      colDataOddania.setCellValueFactory(new PropertyValueFactory<>("dataOddania"));

      colDataCzasUtworzenia.setCellFactory(column -> new TableCell<>() {
         @Override
         protected void updateItem(LocalDateTime item, boolean empty) {
            super.updateItem(item, empty);
            setText(empty || item == null ? null : dateTimeFormatter.format(item));
         }
      });

      projekty = FXCollections.observableArrayList();
      tblProjekt.setItems(projekty);

      // kolumna edycji
      TableColumn<Projekt, Void> colEdit = new TableColumn<>("Edycja");

      colEdit.setCellFactory(column -> new TableCell<>() {

         private final GridPane pane;

         {
            Button btnTask = new Button("Zadania");
            Button btnEdit = new Button("Edycja");
            Button btnRemove = new Button("Usuń");

            btnTask.setMaxWidth(Double.MAX_VALUE);
            btnEdit.setMaxWidth(Double.MAX_VALUE);
            btnRemove.setMaxWidth(Double.MAX_VALUE);

            btnTask.setOnAction(e -> openZadanieFrame(getCurrentProjekt()));
            btnEdit.setOnAction(e -> edytujProjekt(getCurrentProjekt()));
            btnRemove.setOnAction(e -> usunProjekt(getCurrentProjekt()));

            pane = new GridPane();
            pane.setAlignment(Pos.CENTER);
            pane.setHgap(5);
            pane.setVgap(5);
            pane.setPadding(new Insets(5));
            pane.add(btnTask, 0, 0);
            pane.add(btnEdit, 0, 1);
            pane.add(btnRemove, 0, 2);
         }

         private Projekt getCurrentProjekt() {
            return getTableView().getItems().get(getIndex());
         }

         @Override
         protected void updateItem(Void item, boolean empty) {
            super.updateItem(item, empty);
            setGraphic(empty ? null : pane);
         }
      });

      tblProjekt.getColumns().add(colEdit);

      wykonawca.execute(() -> loadPage(search4, pageNo, pageSize));
   }

   // ===== PAGINACJA + WYSZUKIWANIE =====
   private void loadPage(String search4, Integer pageNo, Integer pageSize) {
      try {
         List<Projekt> lista = new ArrayList<>();

         if (search4 != null && !search4.isEmpty()) {

            if (search4.matches("[0-9]+")) {
               Projekt p = projektDAO.getProjekt(Integer.parseInt(search4));
               if (p != null) lista.add(p);

            } else if (search4.matches("^\\d{4}-\\d{2}-\\d{2}$")) {
               lista.addAll(projektDAO.getProjektyWhereDataOddaniaIs(
                     LocalDate.parse(search4), pageNo * pageSize, pageSize));

            } else {
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
         logger.error("Błąd ładowania danych", e);
      }
   }

   // ===== PRZYCISKI =====
   @FXML
   private void onActionBtnSzukaj(ActionEvent e) {
      search4 = txtSzukaj.getText();
      pageNo = 0;
      wykonawca.execute(() -> loadPage(search4, pageNo, pageSize));
   }

   @FXML
   private void onActionBtnDalej(ActionEvent e) {
      pageNo++;
      wykonawca.execute(() -> loadPage(search4, pageNo, pageSize));
   }

   @FXML
   private void onActionBtnWstecz(ActionEvent e) {
      if (pageNo > 0) pageNo--;
      wykonawca.execute(() -> loadPage(search4, pageNo, pageSize));
   }

   @FXML
   private void onActionBtnPierwsza(ActionEvent e) {
      pageNo = 0;
      wykonawca.execute(() -> loadPage(search4, pageNo, pageSize));
   }

   @FXML
   private void onActionBtnOstatnia(ActionEvent e) {
      pageNo = 9999; // uproszczone
      wykonawca.execute(() -> loadPage(search4, pageNo, pageSize));
   }

   @FXML
   private void onActionBtnDodaj(ActionEvent e) {
      edytujProjekt(new Projekt());
   }

   // ===== DODAWANIE / EDYCJA =====
   private void edytujProjekt(Projekt projekt) {

      Dialog<Projekt> dialog = new Dialog<>();
      dialog.setTitle("Edycja");

      TextField txtNazwa = new TextField(projekt.getNazwa());
      TextArea txtOpis = new TextArea(projekt.getOpis());

      DatePicker datePicker = new DatePicker(projekt.getDataOddania());

      GridPane grid = new GridPane();
      grid.setHgap(10);
      grid.setVgap(10);

      grid.add(new Label("Nazwa:"), 0, 0);
      grid.add(txtNazwa, 1, 0);
      grid.add(new Label("Opis:"), 0, 1);
      grid.add(txtOpis, 1, 1);
      grid.add(new Label("Data oddania:"), 0, 2);
      grid.add(datePicker, 1, 2);

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
   }

   // ===== USUWANIE =====
   private void usunProjekt(Projekt projekt) {
      Alert alert = new Alert(AlertType.CONFIRMATION);
      alert.setHeaderText("Usunąć projekt?");
      alert.setContentText(projekt.getNazwa());

      Optional<ButtonType> result = alert.showAndWait();

      if (result.isPresent() && result.get() == ButtonType.OK) {
         wykonawca.execute(() -> {
            projektDAO.deleteProjekt(projekt.getProjektId());
            Platform.runLater(() -> projekty.remove(projekt));
         });
      }
   }

   private ZadanieDAO zadanieDAO = new com.project.dao.ZadanieDAOImpl();

   // ===== ZADANIA (Zadanie 6.14) =====
   private void openZadanieFrame(Projekt projekt) {
      try {
         javafx.fxml.FXMLLoader loader = new javafx.fxml.FXMLLoader(getClass().getResource("/fxml/ZadanieFrame.fxml"));
         loader.setControllerFactory(c -> new ZadanieController(projekt, zadanieDAO, wykonawca));
         
         javafx.stage.Stage stage = new javafx.stage.Stage(javafx.stage.StageStyle.DECORATED);
         stage.initModality(javafx.stage.Modality.APPLICATION_MODAL);
         stage.setTitle("Zadania");
         
         javafx.scene.Scene scene = new javafx.scene.Scene(loader.load());
         scene.getStylesheets().add(getClass().getResource("/css/application.css").toExternalForm());
         
         stage.setScene(scene);
         stage.show();
      } catch (Exception e) {
         logger.error("Błąd otwierania okna zadań", e);
         Alert alert = new Alert(AlertType.ERROR);
         alert.setHeaderText("Błąd");
         alert.setContentText(e.getMessage());
         alert.showAndWait();
      }
   }

   // ===== SHUTDOWN =====
   public void shutdown() {
      if (wykonawca != null) {
         wykonawca.shutdown();
         try {
            if (!wykonawca.awaitTermination(5, TimeUnit.SECONDS)) {
               wykonawca.shutdownNow();
            }
         } catch (InterruptedException e) {
            wykonawca.shutdownNow();
         }
      }
   }
}