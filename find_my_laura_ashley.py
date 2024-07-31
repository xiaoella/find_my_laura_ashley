import get_data
import predict 
import send_email

def main():
    
    get_data.main()
    predict.main()
    send_email.main()

    return None

if __name__ == "__main__":
    main()