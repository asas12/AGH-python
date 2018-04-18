import string

VARS = string.ascii_lowercase
VARS = VARS.join(string.ascii_uppercase)
VARS = VARS.join("0123456789")
CONST = "".join("01")
OPS = "=|&>^"


def validate(expr):
    """Sprawdza poprawność syntaktyczną wyrażenia oraz zwraca je sparsowane, a także zmienne"""
    used_vars = {}
    resulting_expr = []
    variable = ""
    state = 1  # oczekiwana "~", znak, stała, lub lewy nawias
    par_count = 0  # licznik nawiasów
    for char in expr:
        if char == " ":
            if state == 2:
                if variable:
                    used_vars.update({variable: False})
                    resulting_expr.append(variable)
                    variable = ""
        elif state == 1:  # w poprzednim kroku NOT lub OPS
            if char in VARS:
                state = 2
                variable = variable + char
            elif char == "(":
                resulting_expr.append(char)
                par_count += 1
                state = 3
            elif char == "~":
                resulting_expr.append(char)
                continue
            else:
                return False, False
        elif state == 2:  # w poprzednim kroku znak
            if char in VARS:
                state = 2
                variable = variable + char
            elif char in OPS:
                state = 1
                if variable:
                    used_vars.update({variable: False})
                    resulting_expr.append(variable)
                variable = ""
                resulting_expr.append(char)
            elif char == ")":
                par_count -= 1
                state = 4
                if variable:
                    used_vars.update({variable: False})
                    resulting_expr.append(variable)
                variable = ""
                resulting_expr.append(char)
            else:
                return False, False
        elif state == 3:  # w poprzednim kroku "("
            if char in VARS:
                variable = variable.join(char)
                state = 2
            elif char == "(":
                par_count += 1
                resulting_expr.append(char)
            elif char == "~":
                resulting_expr.append(char)
                state = 1
            else:
                return False, False
        elif state == 4:  # w poprzednim kroku ")"
            if char in OPS:
                state = 1
                resulting_expr.append(char)
            elif char == ")":
                par_count -= 1
                resulting_expr.append(char)
            else:
                return False, False
        if par_count < 0:
            return False, False
    if variable:
        used_vars.update({variable: False})
        resulting_expr.append(variable)
    if par_count == 0 and state != 3 and state != 1:  # poprawne wyrażenie musi kończyć sie stanem False i mieć zamknięte wszystkie nawiasy
        return used_vars, resulting_expr
    else:
        return False


def to_rpn(expr, vars):
    '''Przetwarza wyrażenie expr o zmiennych vars w RPN'''
    res = []
    stack = []
    for char in expr:
        if char == " ":
            continue
        if char in vars:
            res.append(char)
        elif char in "=>":
            if stack:
                tmp = stack.pop()
                while tmp in "|&^~=>":
                    res.append(tmp)
                    if stack:
                        tmp = stack.pop()
                    else:
                        break
                else:
                    stack.append(tmp)
            stack.append(char)
        elif char in "|&^":
            if stack:
                tmp = stack.pop()
                while tmp in "|&^~":
                    res.append(tmp)
                    if stack:
                        tmp = stack.pop()
                    else:
                        break
                else:
                    stack.append(tmp)
            stack.append(char)
        elif char == "~":
            if stack:
                tmp = stack.pop()
                while tmp == "~":
                    res.append(tmp)
                    if stack:
                        tmp = stack.pop()
                    else:
                        break
                else:
                    stack.append(tmp)
            stack.append(char)
        elif char == "(":
            stack.append(char)
        elif char == ")":
            if stack:
                tmp = stack.pop()
                while tmp != "(":
                    res.append(tmp)
                    if stack:
                        tmp = stack.pop()
                    else:
                        break
                if stack:
                    tmp = stack.pop()
                    if tmp in OPS:
                        res.append(tmp)
                    else:
                        stack.append(tmp)
    while stack:
        res.append(stack.pop())
    return res


def rpn_solver(args, rpn_expr):
    '''Rozwiązuje wyrażenie w RPN ze zmiennymi args'''
    stack = []
    for char in rpn_expr:
        if char in args:
            stack.append(args[char])
        if char == "~":
            a = stack.pop()
            stack.append(not a)
        if char == "|":
            b = stack.pop()
            a = stack.pop()
            stack.append(a or b)
        if char == "&":
            b = stack.pop()
            a = stack.pop()
            stack.append(a and b)
        if char == ">":
            b = stack.pop()
            a = stack.pop()
            stack.append((not a) or b)
        if char == "=":
            b = stack.pop()
            a = stack.pop()
            stack.append(a == b)
        if char == "^":
            b = stack.pop()
            a = stack.pop()
            stack.append(a != b)
    return stack.pop()


def checker(used_vars, rpn_expr):
    '''Generuje wszystkie maski wyników dla wyrażenia w RPN o zmiennych used_vars'''
    res = []
    zflag = False
    oflag = False
    if '1' in used_vars:
        del used_vars['1']
        oflag = True
    if '0' in used_vars:
        del used_vars['0']
        zflag = True
    size = len(used_vars.keys())
    if size == 0:
        if oflag:
            used_vars.update({'1': True})
        if zflag:
            used_vars.update({'0': False})
        return rpn_solver(used_vars, rpn_expr)
    for i in range(2 ** size):
        mask = i
        for key in used_vars:
            used_vars[key] = bool(mask % 2)
            mask = mask // 2
        if oflag:
            used_vars.update({'1': True})
        if zflag:
            used_vars.update({'0': False})
        #print(used_vars)
        tmp_res = rpn_solver(used_vars, rpn_expr)
        #print(i, "ilość zmiennych:", size, "zmienne:", format(i, '0'+str(size)+'b')[::-1], "wynik", tmp_res)
        if tmp_res:
            res.append(format(i, '0'+str(size)+'b')[::-1])
        if '1' in used_vars:
            del used_vars['1']
        if '0' in used_vars:
            del used_vars['0']
    return res,size


def quine_mccluskey_set(input):
    '''Przygotowuje rekurencję, sprawdza warunki dla danych wejściowych'''
    if input is True:
        return True
    elif input is False:
        return False
    #print("in:", input)
    no_of_vars = len(input[0])
    if no_of_vars == 0: # nic nie spełnia funkcji
        return False
    while no_of_vars%2==0:
        no_of_vars/=2
        if no_of_vars == 0:
            return True # wszystko spełnia funkcję
    input_dict = dict(zip(input[0], [False for i in input[0]]))
    #print("input_dict:", input_dict)
    word_length = input[1]
    result = quine_mccluskey(input[0], word_length, [])
    #print("last res:", result)
    return result


def quine_mccluskey(input, word_length, former_expr):
    '''Rekurencyjna funkcja implementująca algorytm'''
    result = []
    input_dict = dict(zip(input, [False for i in input[0]]))
    for i in range(word_length):
        less_ones = [x for x in input if x.count('1') == i]
        more_ones = [x for x in input if x.count('1') == i+1]
        #print(i, "lo", less_ones)
        #print(i, "mo", more_ones)
        for lo in less_ones:
            for mo in more_ones:
                diff = 0
                ind = 0
                for j in range(len(lo)):
                    if lo[j] != mo[j]:
                        diff += 1
                        ind = j
                if diff == 1:
                    res = list(lo)
                    res[ind] = '*'
                    result.append("".join(res))
                    input_dict[mo] = True
                    input_dict[lo] = True
    result = list(set(result))
    for i in input_dict:
        if not input_dict[i]:
            #print("Can't join:", i)
            former_expr.append(i)
    #print("res:", result, "used:", input_dict, "word_l:", word_length)
    if result:
        return quine_mccluskey(result, word_length, former_expr)
    else:
        return result, word_length, former_expr


def optimizer(result, fun_output):  #f_o from checker
    '''Minimalizuje wynik, kończąc algorytm QM'''
    if result is True:
        return True
    elif result is False:
        return False
    input_dict = dict(zip(fun_output[0], [[] for i in fun_output[0]]))
    results = result[2] #from QM
    for var in fun_output[0]:
        #print("var:", var)
        for res in results:
            i = 0
            count = 0
            for char in var:
                if res[i] == char:
                    count+=1
                elif res[i] == '*':
                    count+=1
                i+=1
            if count == i:
                input_dict[var].append(res)
    #print("ID", input_dict)
    final_res = []
    #while input_dict:
    for var in input_dict:
        i=1
        tmp_mask_list = input_dict[var]
        if len(tmp_mask_list) == i:
            for a in tmp_mask_list:
                final_res.append(a)
                for key in input_dict:
                    if a in input_dict[key]:
                        input_dict[key] = []
        i+=1
    return(final_res)


def to_displayable_format(used_vars, end_res):
    '''Generuje formę odpowiednią do wyświetlenia na ekranie dla wyniku algorytmu'''
    if end_res is True:
        return True
    elif end_res is False:
        return False
    uv = list(used_vars.keys())
    res_masks = set(end_res)
    result = ""
    for var in res_masks:
        i = 0
        for char in var:
            if char == '1':
                result = result+(uv[i])+" "
            elif char == '0':
                result = result+(uv[i])
                result = result+"' "
            i+=1
        result = result+" or "
    result = result[:-3]
    return result


def run(expr):
    '''Funkcja nadzoruje przebieg programu dla expr'''
    print("Minimazing: ", expr)
    (used_vars, new_expr) = validate(expr)
    if used_vars:
        rpn_expr = to_rpn(new_expr, used_vars)
        checker_res = checker(used_vars, rpn_expr)
        qm_res = quine_mccluskey_set(checker_res)
        opt_res = optimizer(qm_res, checker_res)
        result = to_displayable_format(used_vars, opt_res)
        print("Result: ", result)
    else:
        print("Improper format.")


if __name__ == "__main__":
    expr = input("Please write expression you would like to evaluate.")
    run(expr)