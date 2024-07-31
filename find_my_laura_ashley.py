import get_data
import predict 
import send_email
import shutil

def main():
    
    get_data.main()
    predict.main()
    send_email.main()
    shutil.rmtree("etsy_data")

    return None

if __name__ == "__main__":
    main()