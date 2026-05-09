package com.project.controller;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.ExecutorService;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.project.dao.ZadanieDAO;
import com.project.model.Projekt;
import com.project.model.Zadanie;

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
import javafx.stage.Stage;
import javafx.stage.WindowEvent;

public class ZadanieController {
    private static final Logger logger = LoggerFactory.getLogger(ZadanieController.class);

    private final Projekt projekt;
    private final ZadanieDAO zadanieDAO;
    private final ExecutorService wykonawca;

    @FXML private Button btnPowrot;
    @FXML private Label lblTytul;
    @FXML private TableView<Zadanie> tblZadanie;
    @FXML private TableColumn<Zadanie, Integer> colId;
    @FXML private TableColumn<Zadanie, String> colNazwa;
    @FXML private TableColumn<Zadanie, String> colOpis;
    @FXML private TableColumn<Zadanie, Integer> colKolejnosc;
    @FXML private TableColumn<Zadanie, LocalDateTime> colDataCzasUtworzenia;

    private ObservableList<Zadanie> zadania;
    private static final DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    public ZadanieController(Projekt projekt, ZadanieDAO zadanieDAO, ExecutorService wykonawca) {
        this.projekt = projekt;
        this.zadanieDAO = zadanieDAO;
        this.wykonawca = wykonawca;
    }

    @FXML
    public void initialize() {
        lblTytul.setText("Zadania dla projektu: " + projekt.getNazwa());

        colId.setCellValueFactory(new PropertyValueFactory<>("zadanieId"));
        colNazwa.setCellValueFactory(new PropertyValueFactory<>("nazwa"));
        colOpis.setCellValueFactory(new PropertyValueFactory<>("opis"));
        colKolejnosc.setCellValueFactory(new PropertyValueFactory<>("kolejnosc"));
        colDataCzasUtworzenia.setCellValueFactory(new PropertyValueFactory<>("dataCzasUtworzenia"));

        colDataCzasUtworzenia.setCellFactory(column -> new TableCell<>() {
            @Override
            protected void updateItem(LocalDateTime item, boolean empty) {
                super.updateItem(item, empty);
                setText(empty || item == null ? null : dateTimeFormatter.format(item));
            }
        });

        zadania = FXCollections.observableArrayList();
        tblZadanie.setItems(zadania);

        TableColumn<Zadanie, Void> colEdit = new TableColumn<>("Akcje");
        colEdit.setCellFactory(column -> new TableCell<>() {
            private final GridPane pane;
            {
                Button btnEdit = new Button("Edycja");
                Button btnRemove = new Button("Usuń");

                btnEdit.setMaxWidth(Double.MAX_VALUE);
                btnRemove.setMaxWidth(Double.MAX_VALUE);

                btnEdit.setOnAction(e -> edytujZadanie(getCurrentZadanie()));
                btnRemove.setOnAction(e -> usunZadanie(getCurrentZadanie()));

                pane = new GridPane();
                pane.setAlignment(Pos.CENTER);
                pane.setHgap(5);
                pane.setVgap(5);
                pane.setPadding(new Insets(5));
                pane.add(btnEdit, 0, 0);
                pane.add(btnRemove, 0, 1);
            }

            private Zadanie getCurrentZadanie() {
                return getTableView().getItems().get(getIndex());
            }

            @Override
            protected void updateItem(Void item, boolean empty) {
                super.updateItem(item, empty);
                setGraphic(empty ? null : pane);
            }
        });

        tblZadanie.getColumns().add(colEdit);

        wykonawca.execute(this::loadZadania);
    }

    private void loadZadania() {
        try {
            List<Zadanie> lista = zadanieDAO.getZadania(projekt.getProjektId());
            Platform.runLater(() -> {
                zadania.clear();
                zadania.addAll(lista);
            });
        } catch (Exception e) {
            logger.error("Błąd ładowania zadań", e);
            Platform.runLater(() -> showError("Błąd ładowania", e.getMessage()));
        }
    }

    @FXML
    private void onActionBtnPowrot(ActionEvent event) {
        Stage stage = (Stage) btnPowrot.getScene().getWindow();
        stage.fireEvent(new WindowEvent(stage, WindowEvent.WINDOW_CLOSE_REQUEST));
    }

    @FXML
    private void onActionBtnDodaj(ActionEvent event) {
        Zadanie z = new Zadanie();
        z.setProjektId(projekt.getProjektId());
        edytujZadanie(z);
    }

    private void edytujZadanie(Zadanie zadanie) {
        Dialog<Zadanie> dialog = new Dialog<>();
        dialog.setTitle("Edycja Zadania");

        TextField txtNazwa = new TextField(zadanie.getNazwa() != null ? zadanie.getNazwa() : "");
        TextArea txtOpis = new TextArea(zadanie.getOpis() != null ? zadanie.getOpis() : "");
        TextField txtKolejnosc = new TextField(zadanie.getKolejnosc() != null ? zadanie.getKolejnosc().toString() : "0");

        GridPane grid = new GridPane();
        grid.setHgap(10);
        grid.setVgap(10);
        grid.add(new Label("Nazwa:"), 0, 0);
        grid.add(txtNazwa, 1, 0);
        grid.add(new Label("Opis:"), 0, 1);
        grid.add(txtOpis, 1, 1);
        grid.add(new Label("Kolejność:"), 0, 2);
        grid.add(txtKolejnosc, 1, 2);

        dialog.getDialogPane().setContent(grid);
        ButtonType ok = new ButtonType("Zapisz", ButtonBar.ButtonData.OK_DONE);
        dialog.getDialogPane().getButtonTypes().addAll(ok, ButtonType.CANCEL);

        dialog.setResultConverter(btn -> {
            if (btn == ok) {
                zadanie.setNazwa(txtNazwa.getText());
                zadanie.setOpis(txtOpis.getText());
                try {
                    zadanie.setKolejnosc(Integer.parseInt(txtKolejnosc.getText()));
                } catch (NumberFormatException e) {
                    zadanie.setKolejnosc(0);
                }
                return zadanie;
            }
            return null;
        });

        Optional<Zadanie> result = dialog.showAndWait();
        result.ifPresent(z -> wykonawca.execute(() -> {
            try {
                zadanieDAO.setZadanie(z);
                Platform.runLater(() -> {
                    if (!zadania.contains(z)) zadania.add(z);
                    tblZadanie.refresh();
                });
            } catch (Exception e) {
                logger.error("Błąd podczas zapisu zadania", e);
                Platform.runLater(() -> showError("Błąd zapisu", e.getMessage()));
            }
        }));
    }

    private void usunZadanie(Zadanie zadanie) {
        Alert alert = new Alert(AlertType.CONFIRMATION);
        alert.setHeaderText("Usunąć zadanie?");
        alert.setContentText(zadanie.getNazwa());

        Optional<ButtonType> result = alert.showAndWait();
        if (result.isPresent() && result.get() == ButtonType.OK) {
            wykonawca.execute(() -> {
                try {
                    zadanieDAO.deleteZadanie(zadanie.getZadanieId());
                    Platform.runLater(() -> zadania.remove(zadanie));
                } catch (Exception e) {
                    logger.error("Błąd podczas usuwania", e);
                    Platform.runLater(() -> showError("Błąd usuwania", e.getMessage()));
                }
            });
        }
    }

    private void showError(String header, String content) {
        Alert alert = new Alert(AlertType.ERROR);
        alert.setTitle("Błąd");
        alert.setHeaderText(header);
        alert.setContentText(content);
        alert.showAndWait();
    }
}
