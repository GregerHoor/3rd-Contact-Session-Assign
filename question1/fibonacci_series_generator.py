def fibonacci_series(n):
    a, b = 0, 1
    
    all_nums = []
    sum_all_nums = int(0)
    for x in range(n):
        fs_num = a
        all_nums.append(fs_num)
        sum_all_nums += int(fs_num)
        a, b = b, a + b
        
    print('\nList of', n, 'fibonacci num =', all_nums)
    print('Sum of', n, 'fibonacci num =', sum_all_nums)



def main():
    while True:
        num = int(input("\nInput the number you want your fibonacci series to be generated at (Enter '0' to cancel): "))
        
        if num == 00:
            break
        
        if num > 0:
            fibonacci_series(num)
        
        again = input('\nDo you want to try again? (Enter y/n)').strip().lower()
        
        if again == 'y':
            continue
        elif again == 'n':
            break
        



if __name__ == "__main__":
    main()