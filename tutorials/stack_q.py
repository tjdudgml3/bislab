def operate(in_string):
    stack = []
    temp = 0
    in_string = list(in_string)
    while(in_string):
        digit = in_string.pop(0)
        
        if digit == "+" or digit == "-" :
            stack.append(digit)
        elif digit == "*":
            temp = int(stack.pop()) * int(in_string.pop(0))
            stack.append(temp)
        elif digit == "/":
            temp = int(stack.pop()) / int(in_string.pop(0))
            stack.append(int(temp))
        elif digit == "%":
            temp = int(stack.pop()) % int(in_string.pop(0))
            stack.append(int(temp))
        else:
            stack.append(digit)
    # print(f"operate_stack: {stack}")       
    result = stack.pop(0)
    
    while(stack):
        oper = stack.pop(0)
        # print(oper, result)
        if oper == "+":
            result = int(result) + int(stack.pop(0))
        elif oper == "-":
            result = int(result) -int(stack.pop(0))
        # print(result)
        
    return result

def solution(in_string):
    stack = []
    in_string = list(in_string)
    while(in_string):
        digit = in_string.pop(0)
        if digit == "(":
            temp_stack = []
            while(True):
                digit = in_string.pop(0)
                if digit ==")":
                    break
                temp_stack.append(digit)
            # print(temp_stack)
            digit = operate(temp_stack)
               
        stack.append(str(digit))
    # print(stack)
    result = operate(stack)
    return result
    
while(True):
    print(solution(input()))














        
    