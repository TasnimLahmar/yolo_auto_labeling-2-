import ultralytics
import os
from ultralytics.data.annotator import auto_annotate

def main():
    auto_annotate(
        data=r"C:\Users\ASUS\Desktop\lot10\compare_data7\images",
        det_model=r"C:\Users\ASUS\Desktop\50_epochs.pt",
        output_dir=r"C:\Users\ASUS\Desktop\lot10\compare_data7\data7_200_preds"
    )


if __name__ == "__main__":
    main()