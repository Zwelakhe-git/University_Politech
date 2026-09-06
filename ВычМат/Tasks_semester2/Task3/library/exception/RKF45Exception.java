package library.exception;

public class RKF45Exception extends Exception {
    
    // Конструктор по умолчанию
    public RKF45Exception() {
        super("Ошибка в методе RKF45");
    }
    
    // Конструктор с сообщением об ошибке
    public RKF45Exception(String message) {
        super(message);
    }
    
    // Конструктор с сообщением и причиной ошибки
    public RKF45Exception(String message, Throwable cause) {
        super(message, cause);
    }
    
    // Конструктор с причиной ошибки
    public RKF45Exception(Throwable cause) {
        super(cause);
    }
}
