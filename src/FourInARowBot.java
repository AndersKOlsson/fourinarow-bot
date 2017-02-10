import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class FourInARowBot {

    private Scanner scan = new Scanner(System.in);

    public void run() {
        final Map settings = new HashMap<String, String>();
        while(scan.hasNextLine()) {
            String line = scan.nextLine();
            if (line.isEmpty()) {
                String[] parts = line.split(" ");

                switch (parts[0]) {
                    case "settings":
                        settings.put(parts[1], parts[2]);
                        break;
                    case "update":
                        // store game updates
                        break;
                    case "action":
                        System.out.println("place_disc 0");
                        System.out.flush();
                        break;
                    default:
                        System.err.println("Got unknown action: " + parts[0]);
                }
            }
        }
    }

    public static void main(String[] args) {
        (new FourInARowBot()).run();
    }
}
