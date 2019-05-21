from src.hufman.hufman_algo import compress_to_file, decompress_from_file

if __name__ == '__main__':
    filename = 'C:/W/controlsSystemOptimisationMethods/resources/out.hfm'
    with open('C:/W/controlsSystemOptimisationMethods/resources/in', 'rb') as inp:
        data = inp.read()
        compress_to_file(data, filename)
    # with open(filename, 'rb') as out:
    data = decompress_from_file(filename)
    print(data)
# with open('C:/W/controlsSystemOptimisationMethods/resources/wn.png', 'wb') as out:
#     pass
