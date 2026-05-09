package com.project.app;

import com.project.controller.ProjectController;
import com.project.dao.ProjektDAO;
import com.project.dao.ProjektDAOImpl;
import com.project.datasource.DbInitializer;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.stage.Stage;

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

      stage.setOnCloseRequest(e -> {
         controller.shutdown();
         Platform.exit();
      });

      stage.setTitle("Projekty");
      stage.setScene(scene);
      stage.show();
   }

   public static void main(String[] args) {
      DbInitializer.init();
      launch(args);
   }
}