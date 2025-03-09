def read_parameters(filename):
    """ Reads parameters from a text file and returns them as a dictionary. """
    params = {}
    with open(filename, 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=')
                # Typecast as int if alpha or N
                if '.' in value or key.strip() in ['alpha', 'N']:
                    params[key.strip()] = float(value.strip())
                # String if function of mean camber line
                elif key.strip() == 'f1':
                    params[key.strip()] = value.strip()
                # Otherwise, typecast as int
                else:
                    params[key.strip()] = int(value.strip())
    return params