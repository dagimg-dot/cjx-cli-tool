import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;

public class App extends Application {
    public static void main(String[] args) throws Exception {
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) throws Exception {
        StackPane root = new StackPane();
        primaryStage.setTitle("Hello World");
        Button btn = new Button();
        btn.setText("Say 'Hello World'");
        btn.setOnAction(e -> System.out.println("Hello World!"));
        root.getChildren().add(btn);
        primaryStage.setScene(new Scene(root, 800, 600));
        primaryStage.show();
    }
}
