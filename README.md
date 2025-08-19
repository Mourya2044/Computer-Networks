# Error Detection using Checksum and CRC

This project implements two common error detection techniques used in computer networks: Checksum and Cyclic Redundancy Check (CRC). The sender module reads data from a file, calculates the codeword using the selected method (Checksum or CRC), and sends it to the receiver. The receiver then verifies the integrity of the received data. An error injection module is also included to simulate data corruption during transmission.

## Features

- **Checksum**: Implements the basic checksum algorithm for error detection.
- **Cyclic Redundancy Check (CRC)**: Implements CRC with a choice of standard polynomials (CRC-8, CRC-10, CRC-16, CRC-32).
- **Sender/Receiver Model**: Demonstrates a client-server architecture for data transmission.
- **Error Injection**: Simulates transmission errors to test the effectiveness of the error detection methods.

## File Descriptions

- **`sender.py`**: Reads data from a file, computes the codeword using either Checksum or CRC, and sends it to the receiver. It can also be configured to inject errors into the data before transmission.
- **`reciever.py`**: Listens for incoming connections from the sender, receives the data, and verifies its integrity using the appropriate error detection method.
- **`checksum.py`**: Contains the functions for generating and verifying the checksum.
- **`crc.py`**: Contains the functions for generating and verifying the CRC.
- **`injecterror.py`**: A utility to randomly introduce errors into the transmitted data.
- **`data.txt`**: A sample data file to be used as input for the sender.

## How to Use

1.  **Start the receiver:**
    Open a terminal and run the following command to start the receiver server:
    ```sh
    python reciever.py
    ```
    The receiver will start listening for incoming connections on `localhost:3000`.

2.  **Run the sender:**
    Open another terminal and run the `sender.py` script with the following arguments:

    -   **For Checksum:**
        ```sh
        python sender.py data.txt checksum
        ```
    -   **For CRC:**
        Choose a CRC polynomial from the available options (`CRC-8`, `CRC-10`, `CRC-16`, `CRC-32`) and run the command:
        ```sh
        python sender.py data.txt crc CRC-16
        ```

3.  **Observe the output:**
    -   The sender terminal will show the data being sent.
    -   The receiver terminal will display the received data and whether it is valid or not.
