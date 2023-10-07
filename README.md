# ClientServer_Network
Client/Server Network for dictionary exchange in binary, JSON and XML formats, with built-in encryption for text files
## Introduction

The project is a robust client-server application designed to securely transmit dictionaries and text files between users. The client can share a dictionary exchange in binary, JSON, and XML formats, with built-in encryption for text files. The application allows users to create a dictionary, populate it, serialize it, and send it to a server. Users can also create a text file and send it to the server. The client-side offers the flexibility to choose the pickling format (binary, JSON, or XML) for the dictionary and the option to encrypt text in a text file. On the server-side, there is a configurable option to print the contents of received items to the screen and/or to a file. The server is also equipped to handle encrypted contents.

## Technologies Used

This project leverages various technologies and libraries, including:

- **Python**: The primary programming language used for both the client and server applications.
- **Socket Programming**: For network communication between the client and server.
- **Serialization Libraries**:
  - `pickle`: For binary serialization.
  - `json`: For JSON serialization.
  - `xml.etree.ElementTree`: For XML serialization.
- **Encryption**:
  - `Crypto.Cipher`: For AES encryption (cryptography library).
- **Progress Bar Display**: The `tqdm` library is used for displaying progress bars during data transmission.

## Installation

Before running the application, ensure you have Python installed on your system. Additionally, some libraries may need to be installed. Use `pip` to install the required dependencies:

```bash
pip install tqdm pycryptodome dict2xml
```

## Running the Program

### Windows

1. Open a command prompt.

2. Navigate to the project's `src` directory:
   ```bash
   cd path\to\project\src
   ```

3. Start the server by running:
   ```bash
   python server.py
   ```

4. Open another command prompt and navigate to the `src` directory.

5. Run the client application:
   ```bash
   python client.py
   ```

### MacOS and Linux

1. Open a terminal.

2. Navigate to the project's `src` directory:
   ```bash
   cd /path/to/project/src
   ```

3. Start the server by running:
   ```bash
   python server.py
   ```

4. Open another terminal and navigate to the `src` directory.

5. Run the client application:
   ```bash
   python client.py
   ```

## Configuration

The server's behavior can be configured by editing the server configuration file (not provided). Configuration options may include the listening port, whether to print to the screen, whether to save to a file, and the file path for saving.

## Encryption

Both the server and client use AES encryption with a shared key (`KEY`) and nonce (`NONCE`). Replace these placeholders with your own secret values for security.

## Testing

This project includes test suites (`test_client` and `test_server`) for validating the client and server functionalities.

### Running Client Tests

To run the client test suite, follow these steps:

1. Open a terminal/command prompt.

2. Navigate to the `src` directory of the project:
   ```bash
   cd path\to\project\src
   ```

3. Run the client test suite:
   ```bash
   python -m unittest test_client.py
   ```

### Running Server Tests

The server tests will be similar to the client tests. You can create a `test_server.py` file with similar test cases for the server-side functionalities. Then, to run the server test suite:

1. Open a terminal/command prompt.

2. Navigate to the `src` directory of the project:
   ```bash
   cd path\to\project\src
   ```

3. Run the server test suite:
   ```bash
   python -m unittest test_server.py
   ```

Ensure that you have the necessary test data and mock objects set up for accurate testing.

## Conclusion

This Client/Server Network application offers a versatile and secure platform for exchanging dictionaries and text files between clients and servers. Users have the flexibility to choose serialization formats and encryption options to meet their specific needs. Please refer to the source code and configuration files for further customization and integration into your projects.

## Contribution Guidelines 

We welcome contributions from the community to enhance the project further. If you'd like to contribute, please follow these guidelines:

1. Fork the Repository: Fork the project to your GitHub account.

2. Create a Branch: Create a feature branch for your contributions.

3. Commit Changes: Make your changes, commit them to your branch, and provide clear commit messages.

4. Push to Your Fork: Push your changes to your forked repository on GitHub.

5. Open a Pull Request: Create a pull request from your forked repository to the main project repository.

6. Review and Collaborate: Collaborate with maintainers and address any feedback during the review process.

## License 
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements 

We would like to express our gratitude to the open-source community and the developers of the libraries and tools that make this project possible.
