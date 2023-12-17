#BWT to transform data
def burrows_wheeler_transform(text):
    rotations = [text[i:] + text[:i] for i in range(len(text))]
    sorted_rotations = sorted(rotations)
    bwt = ''.join(rot[-1] for rot in sorted_rotations)    
    return bwt


#Inverse BWT to reconstruct original data
def inverse_burrows_wheeler_transform(bwt):
    table = [''] * len(bwt)    
    for i in range(len(bwt)):
        table = sorted([bwt[i] + table[i] for i in range(len(bwt))])
    original_text = [s for s in table if s.endswith('$')][0]    
    return original_text.rstrip('$')


def main(text):
    print(text)
    text += "$"
    transformed_text = burrows_wheeler_transform(text)
    print(transformed_text)
    original_text = inverse_burrows_wheeler_transform(transformed_text)
    print(original_text)
