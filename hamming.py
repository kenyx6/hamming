# Original code: https://replit.com/@jlpicard/Hamming74-1

# Objective: Improve the function 'hamming_decode' by making it more generic (= can work with any version of hamming).

# How to do: This can be achieved by multiplying a calculated "R matrix" with the hamming-encoded message.
# You do not need to calculate R at the moment.

# Hint: look at hamming_encode()

###############################################################
# Hamming(7,4) PROJECT
# May 2021

# We will use the random library to generate random messages
# and introduce errors at random locations.
import random


# Hamming is best encoded / decoded using matrix operations
# Multiplying matrixes could be achieved using a library such as numpy
# or code such as this one
def matrix_multi(lista, listb):
    return [a*b for a, b in zip(lista, listb)]


######################## Matrix generation ############################
# The following functions are "dummies", fakely generatring
# matrixes usefull with Hamming encoding / decoding
# Encoding matrix
def generate_G(nb_parity_bits=3):
    # P1 = parity(D1, D2, D4)
    # P2 = parity(D1, D3, D4)
    # P3 = parity(D2, D3, D4)
    G = [
        [1, 1, 0, 1],
        [1, 0, 1, 1],
        [1, 0, 0, 0],
        [0, 1, 1, 1],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]

    return G


# Parity-check matrix H
def generate_H(nb_parity_bits=3):
    H = [
        [1, 0, 1, 0, 1, 0, 1],
        [0, 1, 1, 0, 0, 1, 1],
        [0, 0, 0, 1, 1, 1, 1]
    ]
    return H


# Parity-check matrix H's translation Ht
def generate_Ht(nb_parity_bits=3):
    Ht = [
        [1, 0, 0],
        [0, 1, 0],
        [1, 1, 0],
        [0, 0, 1],
        [1, 0, 1],
        [0, 1, 1],
        [1, 1, 1]
    ]
    return Ht


# Return message matrix
def generate_R(nb_parity_bits=3):
    R = [
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1]
    ]

    return R


def transpose(matrix):  # make matrix transposed
    return list(zip(*matrix))


def get_bin_factor(num, bits):  # get the bin factors, lower is first
    answer = []
    for step in range(bits):
        answer.append(num % 2)
        num = num >> 1
    return answer


def make_matrix_g_r(data_len, check_len):
    # get data position
    data_dict = {}
    ipower = 0
    idata = 0
    for i in range(1, data_len+check_len+1):
        if i == (1 << ipower):
            ipower += 1
        else:
            data_dict[i] = idata
            idata += 1
    print('data position is:', data_dict)

    print('Matrix G is:')
    G = []
    ipower = 0
    for i in range(1, data_len+check_len+1):
        if i in data_dict:
            member = [0] * data_len  # initial all zero
            member[data_dict[i]] = 1
        else:
            member = [get_bin_factor(x, check_len)[ipower] for x in data_dict]
            ipower += 1
        print(i, member)
        G.append(member)

    print('Matrix R is:')
    R = []
    for i in range(data_len):
        member = [0] * (data_len+check_len)  # initial all zero
        for x in data_dict:
            if i == data_dict[x]:
                member[x-1] = 1
                print(member)
                break
        R.append(member)
    return G, R


def make_matrix_ht(check_len):
    Ht = []
    for i in range(1, 1 << check_len):
        member = get_bin_factor(i, check_len)
        Ht.append(member)
    return Ht


# Get parity bits
def find_pb(digits):
    answer = 1
    for iposi in range(1, digits+5):
        x = 1 << iposi
        if x >= (digits + iposi + 1):
            answer = iposi
            break
    return answer


###################### HELPER FUNCTIONS ########################
# Conversion of a binary list to an integer
# eg.: [ 1, 1, 0 ] -> 6
def binlist_to_int(lista):
    result = 0
    for digit in lista:
        result = (result << 1) | digit
    return result


###################### HAMMING(7, 4) ENCODER ########################
def hamming_encode(message, G=None, nb_parity_bits=3):
    if not G:
        G = generate_G(nb_parity_bits)
    hamming = []
    for i in G:
        message_and_G = matrix_multi(i, message)
        bit = message_and_G.count(1) % 2
        hamming.append(bit)

    return hamming


##################### CHANNEL-ADDED ERROR (1 bit) ######################
def flip_bit(message, location):
    # This will flip the bit at position e-1 (0->1 and 1->0)
    message[location] = 1 - message[location]

    return message
    

def flip_random_bit(message):
    e = random.randint(1, len(message))
    print("Flipping bit (=introducing error) at location: " + str(e))

    # This will flip the bit at position e-1 (0->1 and 1->0)
    message = flip_bit(message, e-1)

    return message


####################### HAMMING(7,4) DECODER #######################
def hamming_find_error(hamming, Ht, nb_parity_bits=3):
    if not Ht:
        Ht = generate_Ht(nb_parity_bits)
        print('Matrix Ht is:')
        print(Ht)
        print('-'*40)
        # H = generate_H(nb_parity_bits)
    H = transpose(Ht)
    print('Matrix H is:')
    print(H)
    print('-' * 40)
    # Finding the location of any potential error
    error_location_in_Ht_list = []
    # Matrix multiplication between H and the message
    #  + checking the parity
    # This will indicate which row in Ht indicates the location of the error
    for i in H:
        parity = matrix_multi(i, hamming).count(1) % 2
        error_location_in_Ht_list.append(parity)

    error_location_in_Ht = binlist_to_int(error_location_in_Ht_list) - 1

    # If any parity bit is set to 1, it means there was an error.
    # The value of the each parity bit can provide the location of the
    # wrong bit.
    if error_location_in_Ht >= 0:
        error_location_in_hamming = binlist_to_int(Ht[error_location_in_Ht])
    else:
        error_location_in_hamming = 0
    print('Where did we find an error? ' + str(error_location_in_hamming))

    return error_location_in_hamming


# Correct any error in the hamming encoded message
# This function will CHANGE the hamming variable as well
def hamming_correct(hamming, Ht=None, nb_parity_bits=3):
    error_location = hamming_find_error(hamming, Ht, nb_parity_bits)

    # If there was an error, correct it by swapping the corresponding bit
    if error_location > 0:
        flip_bit(hamming, error_location - 1)

    return hamming


########################################
######## IMPROVE THIS FUNCTION #########
########################################
def hamming_decode(hamming, R=None, nb_parity_bits=3):
    if not R:
        R = generate_R(nb_parity_bits)

    # The error corrected message is the concatenation of bits 2, 4, 5 and 6
    # result = [hamming[2], hamming[4], hamming[5], hamming[6]]

    result = []
    for position in R:
        bits = matrix_multi(position, hamming).count(1) % 2
        result.append(bits)

    return result


##################### MAIN PROGRAM #####################
# Generate a random string of "0" and "1"

# Change data length here!
data_len = 5
# Change data length here!

para_r = find_pb(data_len)
print('Data length is:', data_len, 'nb_parity_bits is:', para_r)

Ht = make_matrix_ht(para_r)
G, R = make_matrix_g_r(data_len, para_r)

# G, Ht, R = None, None, None

message = [random.getrandbits(1) for x in range(data_len)]

# Or use a predetermined message
# message = [1, 0, 1, 0]

print("Message: " + str(message))

hamming = hamming_encode(message, G)
print("Encoded hamming message: " + str(hamming))

hamming_with_error = flip_random_bit(hamming)
print("Received hamming message: " + str(hamming_with_error))

corrected_message = hamming_correct(hamming_with_error, Ht)
print('Corrected hamming message: ' + str(corrected_message))

decoded_message = hamming_decode(corrected_message, R)
print('Corrected message: ' + str(decoded_message))
