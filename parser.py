# Imports:
import os

# Global Variables:
TEST = False
FILE_TEST = False
LEXICAL_CHAR_TEST = False
LEXICAL_TOKEN_TEST = False
TEST_CHAR = False

OUTPUT_FILE = open("parser_output.txt", "w")
CHARACTER_ARRAY = []
CHARACTER_INDEX = 0
CURRENT_CHAR = []
CURRENT_CHAR_NUM = 0
CURRENT_LINE = 1
BREAKER = "___________________________________________________________"

# Defined Functions:
# Lexical Analyzer
def lexical_analyzer(file_content):
    """Tokenizes the input file content into characters with categories."""
    global CHARACTER_INDEX
    CHARACTER_INDEX = 0
    file_character_array = []
    for line in file_content:
        for char in line:
            if char.isalpha() or char == "_":
                category = "Lower-alpha" if char.islower() else "Upper-alpha"
                file_character_array.append([char, category])
            elif char.isdigit():
                file_character_array.append([char, "Digit"])
            elif char in ",.-|'?:*=+/\^~$&()[]<>":
                category = categorize_special_char(char)
                file_character_array.append([char, category])
            elif char == "\n":
                file_character_array.append([char, "New-Line"])
    global CHARACTER_ARRAY
    CHARACTER_ARRAY = file_character_array

def categorize_special_char(char):
    """Categorizes special characters."""
    return {
        ",": "Comma",
        ".": "Period",
        "-": "Minus_op",
        "|": "Bar",
        "'": "Quote",
        "?": "Question",
        ":": "Colon",
        "*": "Mult_op",
        "=": "Equal_op",
        "+": "Plus_op",
        "/": "Front-Slash",
        "\\": "Back-Slash",
        "^": "Caret",
        "~": "Tilde",
        "$": "Dollar",
        "&": "Ampersand",
        "(": "Bracket-Open",
        ")": "Bracket-Close",
        "[": "Square-Bracket-Open",
        "]": "Square-Bracket-Close",
        "<": "Angle-Bracket-Open",
        ">": "Angle-Bracket-Close",
    }.get(char, "Unknown")
        
 # Getting next lexeme:

def get_next_lexeme():
    """ Returns the next token in the array while increasing index and ignores whitespace"""
    global CHARACTER_ARRAY, CURRENT_CHAR, CHARACTER_INDEX, CURRENT_LINE, CURRENT_CHAR_NUM
    CURRENT_CHAR = CHARACTER_ARRAY[CHARACTER_INDEX]
    CURRENT_CHAR_NUM +=1
    CHARACTER_INDEX +=1
    if TEST_CHAR == True:
        print(CURRENT_CHAR)
    if (CURRENT_CHAR[0] == "\n"):
        CURRENT_LINE +=1
        CURRENT_CHAR_NUM = 0
        get_next_lexeme()
    elif (CURRENT_CHAR[0] == " "):
        get_next_lexeme() 
    
def get_prev_lexeme():
    """ Returns the next token in the array while increasing index and returns whitespace"""
    global CHARACTER_ARRAY, CURRENT_CHAR, CHARACTER_INDEX, CURRENT_LINE
    CURRENT_CHAR = CHARACTER_ARRAY[CHARACTER_INDEX-1]
    CHARACTER_INDEX -=1
    if (CURRENT_CHAR[0] == "\n"):
        CURRENT_LINE -=1
        get_prev_lexeme() 
               
# Function for Raising Errors:
def raise_error(error, char):
    
    OUTPUT_FILE.write(f"Error Found on line {CURRENT_LINE} at Character {CURRENT_CHAR_NUM} : {error} Found '{char[0]}' instead.\n")
    
    while CURRENT_CHAR[0] != ".":
        try:
            get_next_lexeme()  # Fetch the next lexeme
        except IndexError:
            # Stop if CURRENT_CHAR is out of bounds
            break
    
    # Ensure we fetch one more lexeme after '.' if it's valid
    if CURRENT_CHAR[0] == ".":
        try:
            get_next_lexeme()
        except IndexError:
            pass
    program()


# Functions for Recursive Descent Parser:
# Start Symbol:
def program(): #<program> -> <clause-list> <query> | <query>
    if CHARACTER_ARRAY[0][0] != "?":
        if CURRENT_CHAR[0] == ".":
            return False
        clause_list()
    
    return query()
 

def query(): # <query> 	-> ?- <predicate-list> 
    if CURRENT_CHAR[0] == "?":
        get_next_lexeme()
        if CURRENT_CHAR[0] == "-":
            get_next_lexeme()
            return predicate_list()
    return False
        

def clause_list(): # <clause-list>	 -> <clause> | <clause> <clause-list>
    if clause():
        get_next_lexeme()
        get_next_lexeme()
        if CURRENT_CHAR[0] != "?":
            return clause_list()
        return True
    return False
    
            

def clause(): # <clause> -> <predicate> . | <predicate> :- <predicate-list> .
    if predicate():
        if CHARACTER_ARRAY[CHARACTER_INDEX][0] == ".":
            return True

        if CHARACTER_ARRAY[CHARACTER_INDEX][0] != ":":
            raise_error("Expected '.'",CURRENT_CHAR)
            return False
        else:
            if CHARACTER_ARRAY[CHARACTER_INDEX][0] == ":":
                get_next_lexeme() # going onto :
                if CHARACTER_ARRAY[CHARACTER_INDEX][0] == "-":
                    get_next_lexeme() # Going onto -
                    get_next_lexeme() # Going onto next char

                    if predicate_list():
                        if CHARACTER_ARRAY[CHARACTER_INDEX][0] == ".":
                            return True
                        else:
                            raise_error("Expected '.'",CURRENT_CHAR)
                            return False
    return False
                    

def predicate_list(): # <predicate-list> -> <predicate> | <predicate> , <predicate-list>
    if predicate():
        while CHARACTER_ARRAY[CHARACTER_INDEX][0] == ",":
            get_next_lexeme() # going onto the comma
            get_next_lexeme() # going onto next character
            if not predicate():
                return False
        return True
    return False

def predicate(): # <predicate>	-> <atom> | <atom> ( <term-list> )
    if atom():
        if CHARACTER_ARRAY[CHARACTER_INDEX][0] == "(":
            get_next_lexeme()
            get_next_lexeme()
            if not term_list():
                return False
            if CHARACTER_ARRAY[CHARACTER_INDEX][0] == ")":
                get_next_lexeme()
            if CURRENT_CHAR[0] == ")":
                return True
            else:
                raise_error("Expected )",CURRENT_CHAR)
                return False
        
        return True
    if CURRENT_CHAR[0] != "?":
        raise_error("Expected atom (Starting with small letter or string)",CURRENT_CHAR)
    return False

def structure(): # <structure>	 -> <atom> ( <term-list> )
    if atom():
        if CHARACTER_ARRAY[CHARACTER_INDEX][0] == "(":
            get_next_lexeme()
            get_next_lexeme() # Get onto the next char
            if not term_list():
                return False
            if CHARACTER_ARRAY[CHARACTER_INDEX][0] == ")":
                get_next_lexeme()
            if CURRENT_CHAR[0] == ")":
                return True
            else:
                raise_error("Expected )",CURRENT_CHAR)
                return False
        else:
            return True
    return False  

def term_list(): # <term-list>	-> <term> | <term> , <term-list>
    if term():
        
        while(CHARACTER_ARRAY[CHARACTER_INDEX][0] == "," or CURRENT_CHAR[0] == ","):
            # if CURRENT_CHAR[0] == ")":
            #     break
            if CHARACTER_ARRAY[CHARACTER_INDEX][0] == ",":
                get_next_lexeme() # Get onto the comma
            get_next_lexeme() # Get onto the next char
            if not term():
                raise_error("Expected Term (start with an alphabet/a number)",CURRENT_CHAR)
                return False

        return True
    raise_error("Expected Term(start with an alphabet/a number)",CURRENT_CHAR)
    return False

def term(): # <term> -> <atom> | <variable> | <structure> | <numeral>
    return structure() or variable() or numeral()
      
def atom(): # <atom> -> <small-atom> | ' <string> '
    if small_atom():
        return True
    if CURRENT_CHAR[0] == "'":
        get_next_lexeme()
        if string():
            if CURRENT_CHAR[0] == "'":
                return True
    return False
        

def variable(): # <variable> -> <uppercase-char> | <uppercase-char> <character-list>
    if uppercase():
        character_list()
        return True
    return False

def small_atom(): # <small-atom> -> <lowercase-char> | <lowercase-char> <character-list>
    if lowercase():
        character_list()
        return True
    return False

def string(): # <string> -> <character> | <character> <string>
    if character():
        if not next_character():
            return True
        get_next_lexeme()
        return string()
    return False

def character_list(): # <character-list> -> <alphanumeric> | <alphanumeric> <character-list>
    if alphanumeric():
        if not next_alphanumeric():
            return True
        get_next_lexeme()
        return character_list()
    return False

def character():
    return alphanumeric() or special()

def next_character():
    return next_alphanumeric() or next_special()

def alphanumeric(): #<alphanumeric> -> <lowercase-char> | <uppercase-char> | <digit>
    return lowercase() or uppercase() or digit()

def next_alphanumeric(): #<alphanumeric> -> <lowercase-char> | <uppercase-char> | <digit>
    if CHARACTER_ARRAY[CHARACTER_INDEX][1] == "Lower-alpha" or CHARACTER_ARRAY[CHARACTER_INDEX][1] == "Upper-alpha" or CHARACTER_ARRAY[CHARACTER_INDEX][1] == "Digit":
        return True
    return False

def numeral(): # <numeral> 	-> <digit> | <digit> <numeral>
    if CURRENT_CHAR[1] == "Digit":
        while(CHARACTER_ARRAY[CHARACTER_INDEX][1] == "Digit"):
            get_next_lexeme()
        return True
    return False

# Terminals:

def special(): # <special> 	-> + | - | * | / | \ | ^ | ~ | : | . | ? |  | # | $ | &
    return CURRENT_CHAR[0] in ",.-|'?:*=+/\^~$& "

def next_special(): # <special> 	-> + | - | * | / | \ | ^ | ~ | : | . | ? |  | # | $ | &
    return CHARACTER_ARRAY[CHARACTER_INDEX][0] in ",.-|'?:*=+/\^~$& "

def lowercase(): # <lowercase-char> -> a | b | c | ... | x | y | z 
    return CURRENT_CHAR[1] == "Lower-alpha" 

def uppercase(): # <uppercase-char> -> A | B | C | ... | X | Y | Z | _
    return CURRENT_CHAR[1] == "Upper-alpha" 

def digit(): #<digit> 	-> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
    return CURRENT_CHAR[1] == "Digit"



# Main Function:
def main():
    global OUTPUT_FILE  
    # Main Loop:    
    file_number = 1
    
    while True:
        file_name = f"{file_number}.txt"
        if os.path.isfile(file_name):
            with open(file_name, 'r') as file, open(file_name, 'r') as file_output:
                file_content = file
                OUTPUT_FILE.write(f"Checking file '{file_name}':\n\n")
                
                for index,line in enumerate(file_output):
                    OUTPUT_FILE.write(f"Line {index+1}: {line}")
                OUTPUT_FILE.write("\n\n")
                # Test to check if it reads all files:
                if(TEST and FILE_TEST):   
                    file_content = file.read() 
                    print(f"Contents of {file_name}:\n")
                    print(file_content)
                    print("\n","-" * 20,"\n")  # Separator for clarity
                    
                # Pass file contents to tokenizer:
                lexical_analyzer(file)
                
                # Pass tokens to parser:
                get_next_lexeme()
                is_valid_program = program()
                OUTPUT_FILE.write(f"Valid Program: {is_valid_program}\n{BREAKER}\n\n")
                
                
                global TOKEN_INDEX, CURRENT_LINE
                CURRENT_LINE = 1
                TOKEN_INDEX = 0                    
            file_number += 1
        else:
            OUTPUT_FILE.close()
            if(TEST and FILE_TEST):
                print(f"No file named {file_name} found. Stopping.")
            break



if __name__ == "__main__":
    main()
