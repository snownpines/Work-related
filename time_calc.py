# Assistant worktime @ care recipient calculator
# MK 2017-03
# Developed using Python 3.4

import os


def timespan_to_hours(begin, end):
    """Convert start and end times to amount of hours/minutes"""    
    h_out = 0
    m_out = 0
    
    if end[0] < begin[0]:
        h_out = (24 + end[0]) - begin[0]
    elif end[0] == begin[0]:
        h_out = 0
    elif end[0] > begin[0]:
        h_out = end[0] - begin[0]
    
    if end[1] < begin[1]:
        m_out = (60 + end[1]) - begin[1]
        h_out -= 1
    elif end[1] == begin[1]:
        m_out = 0
    elif end[1] > begin[1]:
        m_out = ((60 + end[1]) - begin[1]) - 60
    
    return h_out, m_out


def format_input(inp_str, span=True):
    """Format input for processing"""
    w_time = False
    
    
    def intify_str(string):
        """Turn time string to tuple with time ints"""
        
        if ',' not in string:
            return (int(string), 0)
        else:
            return (int(string.split(',')[0]), int(string.split(',')[1]))
    
    
    if inp_str.startswith('/'):
        w_time = True
        inp_str = inp_str[1:]
    
    if '*' in inp_str[1:5]:
        multiple_str, inp_str = inp_str.split('*')
        multiple = int(multiple_str)
    else:
        multiple = 1
    
    if span:
        time1_str, time2_str = inp_str.split('-')
        
        time1 = intify_str(time1_str)
        
        time2 = intify_str(time2_str)
        
        return time1, time2, multiple, w_time
    else:
        h_out, m_out = intify_str(inp_str)
        
        return h_out, m_out, multiple, w_time


def sum_list(time_list):
    """Add all times in list together
    
    Add time and wait time separately"""
    h_sum = 0
    m_sum = 0
    w_h_sum = 0
    w_m_sum = 0
    
    for i in time_list:
        
        if i[2]:
            w_h_sum += i[0]
            
            if w_m_sum + i[1] > 59:
                w_h_sum += 1
                w_m_sum = (w_m_sum + i[1]) - 60
            elif w_m_sum + i[1] <= 59:
                w_m_sum += i[1]
        else:
            h_sum += i[0]
            
            if m_sum + i[1] > 59:
                h_sum += 1
                m_sum = (m_sum + i[1]) - 60
            elif m_sum + i[1] <= 59:
                m_sum += i[1]
    return h_sum, m_sum, w_h_sum, w_m_sum


def multiply_time(h_in, m_in, multiple):
    """Multiply amount of time"""
    h_out = 0
    m_out = 0
    
    h_out = h_in * multiple
    
    if m_in * multiple < 60:
        m_out = m_in * multiple
    elif (m_in * multiple) % 60 == 0:
        h_out += (m_in * multiple) // 60
        m_out = 0
    elif m_in * multiple % 60:
        h_out += (m_in * multiple) // 60
        m_out = (m_in * multiple) % 60
    
    return h_out, m_out


def time_by_4(h_in, m_in):
    """Divide time by 4
    
    For use on wait time before adding it to sum total"""
    h_out = 0
    m_out = 0
    ripe_for_div = (h_in * 60) + m_in
    minutes_by_4 = ripe_for_div // 4
    round_num = ripe_for_div / 4 - ripe_for_div // 4
    
    if round_num >= 0.5:
        minutes_by_4 += 1
    
    h_out = minutes_by_4 // 60
    m_out = minutes_by_4 % 60
    
    return h_out, m_out


def time_report():
    """Calculate total time for individual time report
    
    Legit commands:
    'q' exits input mode for time report and prints the sum of hours.
    'del' deletes the last input for time.
    '8,0-9,0' start and stop times. Here the result is 1:00 hour.
    '3*8,0-9,0' same as above but multiplied by 3.
    '/8,0-9,0' or '/3*8,0-9,0' puts the result in the special category
    wait time.
    '8,30', '3*8,30', '/8,30' and so on also work.
    '8-12', '/2*8' for hour only."""
    times_to_add = []
    
    
    def input_result(hours, mins, multiple, w_time):
        """Add time to stack and print time added
        
        index 2 of the tuple that's appended marks time
        as (0) regular time and (1) wait time"""
        nonlocal times_to_add
        
        if multiple > 1:
            hours, mins = multiply_time(hours, mins, multiple)
        
        if w_time:
            times_to_add.append((hours, mins, 1))
            print('{}:{:02} (väntetid)'.format(hours,mins))
        else:
            times_to_add.append((hours, mins, 0))
            print('{}:{:02}'.format(hours, mins))
    
    
    print('\nInputformat ("q" för att sluta/summera): hh,mm-hh,mm\n')
    
    while True:
    
        inp_str = input('tid arbetspass: ')
        
        try:
            if inp_str == 'q':
                break
            
            if inp_str == 'del' and times_to_add and times_to_add[-1][2] == 0:
                print('-arbetstid {0}:{1:02} raderad.'.format(*times_to_add.pop()))
                continue
            elif inp_str == 'del' and times_to_add and times_to_add[-1][2] == 1:
                print('-väntetid {0}:{1:02} raderad.'.format(*times_to_add.pop()))
                continue
            elif inp_str == 'del':
                print('-Det finns inget att radera!')
                continue
            
            if '-' not in inp_str:
                hours, mins, multiple, w_time = format_input(inp_str, span=False)
                input_result(hours, mins, multiple, w_time)
            else:
                start_t, end_t, multiple, w_time = format_input(inp_str)
                hours, mins = timespan_to_hours(start_t, end_t)
                input_result(hours, mins, multiple, w_time)

        except:
            print('\nNu blev det fel\n')
            continue
    
    h_sum, m_sum, wait_h_sum, wait_m_sum = sum_list(times_to_add)
    
    print('\n--Summa arbetstid: {}:{:02}\n'.format(h_sum, m_sum))
    print('--Summa väntetid: {}:{:02}'.format(wait_h_sum, wait_m_sum))
    print('_' * 24)
    return (h_sum, m_sum), (wait_h_sum, wait_m_sum)


def number_of_reports(care_recipient, care_recipient_wt):
    """Give amount of time reports
    
    Counts all time reports that doesn't have
    zeroed tuples, (0, 0), in both lists"""
    reports = 0
    
    for i in range(len(care_recipient)):
        if care_recipient[i] == (0,0) and \
           care_recipient_wt[i] == (0,0):
            pass
        else:
            reports += 1
    
    return reports


def add_hours():
    """Calculate total for hours"""
    times_to_add = []
    
    print('\nInputformat ("q" för att sluta/summera): hh,mm\n')
    
    while True:
        time = input('tid i timmar: ')
        
        if time == 'q':
            break
        
        if ',' in time:
            hours, mins = time.split(',')
            times_to_add.append((int(hours), int(mins), 'Arbetstid'))
            
            print('{}:{:02}'.format(int(hours), int(mins)))
        else:
            hours = int(time)
            times_to_add.append((hours, 0, 'Arbetstid'))
            
            print('{}:00'.format(hours))
    
    h_sum, m_sum, *dev_null = sum_list(times_to_add)
    
    print('\n--Summa timmar: {}:{:02}\n'.format(h_sum, m_sum))
    print('_' * 24)


care_recipient = []
care_recipient_wait_time = []

while True:
    print('\n(1) Lägg till en tidsredovisning')
    print('(2) Avsluta/räkna ihop total arbetad tid hos brukare')
    print('(3) Addera tider fristående')
    print('(4) Radera sista inlagda tidsredovisningen')
    choice = input(': ')
    
    if choice == '1':
        times, wait_times = time_report()
        care_recipient.append(times + (0,))
        care_recipient_wait_time.append(wait_times + (1,))
        continue
    elif choice == '2':
        h_total, m_total, *dev_null = sum_list(care_recipient)
        
        *dev_null, wait_h_total, wait_m_total = \
            sum_list(care_recipient_wait_time)
            
        by_4_wait_h_total, by_4_wait_m_total = \
            time_by_4(wait_h_total, wait_m_total)
        
        work_time = (h_total, m_total, 0)
        wait_time = (by_4_wait_h_total, by_4_wait_m_total, 0)
        
        h_final, m_final, *dev_null = sum_list([work_time, wait_time])
            
        reports = number_of_reports(care_recipient, care_recipient_wait_time)
        
        print('\n--Total arbetstid: {}:{:02}'.format(h_total, m_total))
        print('--Total väntetid (1/4): {}:{:02} ({}:{:02})'.format(wait_h_total, wait_m_total, by_4_wait_h_total, by_4_wait_m_total))
        print('--Summa total: {}:{:02}'.format(h_final, m_final))
        print('--Antal tidsredovisningar: {}'.format(reports))
        print('huvudlistan: ', care_recipient)
        print('väntelistan: ', care_recipient_wait_time)
        print('\n(1) Påbörja inmatning för ny brukare')
        print('(2) Avsluta (fönstret kommer stängas ner!)')
        end_choice = input(': ')
        
        if end_choice == '1':
            care_recipient = []
            care_recipient_wait_time = []
            os.system('cls')
            continue
        elif end_choice == '2':
            break
        else:
            break
    
    elif choice == '3':
        add_hours()
    elif choice == '4' and care_recipient:
        print('\n-Tidsredovisning med arbetstid {}:{:02}'.format(*care_recipient.pop()), end=' ')
        print('och väntetid {}:{:02} raderad!'.format(*care_recipient_wait_time.pop()))
    elif choice == '4':
        print('\n-Det finns inga tidsredovisningar inlagda!')    
    else:
        print('\nOgiltigt val! Försök igen.\n')
