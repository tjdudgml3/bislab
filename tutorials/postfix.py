

def postfix(in_string):
    output = []
    stack = []
    in_string = list(in_string)
    while(in_string):
        # print(stack, output)
        digit = in_string.pop(0)
        if digit == "(":
            stack.append(digit)
        elif digit == "+" or digit == "-":
            while(stack and stack[-1] != "(" ):
                output.append(stack.pop())
            stack.append(digit)
        elif digit == "*" or digit =="/" or digit == "%":
            stack.append(digit)
        elif digit == ")":
            while(stack[-1] != "("):
                output.append(stack.pop())
            stack.pop()
                
        else:
            output.append(digit)
    while(stack):
        output.append(stack.pop())
    
    result = ''
    for a in output:
        result += a
    print(result)
    return result

def get_postfix(in_string):
    in_string = list(in_string)
    stack = []
    operator = ["+", "-", "*", "/", "%"]
    while(in_string):
        # print(stack)
        digit = in_string.pop(0)
        if digit not in operator:
            stack.append(digit)
        else:
            num1 = int(stack.pop())
            num2 = int(stack.pop())
            if digit == "+":
                num1 = num1 + num2
            elif digit == "-":
                num1 = num2 - num1
            elif digit == "*":
                num1 = num1 * num2
            elif digit == "/":
                num1 = num2 / num1
            else:
                num1 = num2 % num1
            stack.append(num1)
    
    return stack[-1]

        
    
while(True):
    print(get_postfix(postfix(input())))
    
