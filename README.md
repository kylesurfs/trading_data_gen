# trading_data_gen
This is a random data generator for trading. The preferred site to use the output from this project is chrt.com

## Installation

To run this program, you need to have Python 3 installed on your machine. You can visit [Python's official website](https://www.python.org/downloads/) to download and install the latest version.

## Usage

To start the program, follow these steps:

1 Open the terminal on your machine.
2 Navigate to the directory where your Python script is located using the cd command cd /path/trading_data_gen.
3 Once you are in the correct directory, type python followed by the name of your script and press enter. It should look like this:

```
python dummyDataCreator.py
```

## Editing

If you would like to edit this project, feel free to do so. The bottom of the script calls two functions whose parameters can be adjusted.

The first is:

```
generate_dummy_data(num_rows)
```
The `generate_dummy_data` function takes an input for `num_rows`, the number of rows of data you want generated. The default is 100 rows.

The second function is:

```
write_to_csv(file_name, headers, data)
```
`write_to_csv()` takes a user input for file_name, and must not include an underscore. An example file_name input might be "dummydata.csv" 


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or suggestions about this project, feel free to contact kylesurfs.