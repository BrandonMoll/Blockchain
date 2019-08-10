import hashlib
import requests

import sys


# TODO: Implement functionality to search for a proof 

def proof_of_work(last_block_string):
    proof = 0

    while valid_proof(last_block_string, proof) is False:
        proof += 1

    return proof

def valid_proof(last_block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?
    """
    guess = f'{last_block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    beg = guess_hash[0:4] #[:6] same thing

    if beg == '0000':
        return True
    else:
        return False


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        r = requests.get(url = node + '/last_block_string')
        data = r.json()
        last_block_string = data['last_block_string']['previous_hash']
        new_proof = proof_of_work(last_block_string)
        
        print(f'found valid proof: {new_proof}')

      
        # TODO: When found, POST it to the server {"proof": new_proof}
        # TODO: We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        proof_data = {'proof': new_proof}
        r = requests.post(url = node+'/mine', json=proof_data)
        data = r.json()

        # TODO: If the server responds with 'New Block Forged'
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print(f'You now have {coins_mined} coins')
        else:
            print('error')
        
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.


