# Assistant worktime @ caretaker calculator
# MK 2017-01
# Developed using Python 3.4

"""
This is just a list (in swe.) of functionality that's implemented, or that
I might add.

--Förbättringar--
Klart! -multiplicera tider: 8*8,0-12,30
Klart! -spara summan för varje blankett och summera totalt för brukare
Klart! -räkna blanketter för brukare
Klart! -särredovisa väntetid? för den ska ju delas på fyra
Klart! -visa antal tidsredovisningar
Klart! -fristående addera tider
Klart! -kunna skriva in tid som antal timmar istället för start-stopp tid
Klart! -inte behöva ange 'komma minut': 7-12
Klart! -undo-funktion för senaste input

-regel för att bara skriva in minuter som 30 eller 03, men inte 3
-minus för att ta bort tid
-uppmärksamma om man matar in något utanför tidsramar: 25,78 etc.

1.input->2.format_input->3.timespan_to_hours->4.save_hours->5.next_2-4_cycle->6.add_hours
"""


def timespan_to_hours(begin, end, multiple):
    """Convert start and end times to time span"""    
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
    
    if multiple > 1:
        h_out, m_out = multiply_time(h_out, m_out, multiple)
    
    return h_out, m_out


def format_input(inp_str, span=True):
    """Format input for processing"""
    w_time = False
    
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
        
        if ',' not in time1_str:
            time1 = (int(time1_str), 0)
        else:
            time1 = (int(time1_str.split(',')[0]), int(time1_str.split(',')[1]))
        if ',' not in time2_str:
            time2 = (int(time2_str), 0)
        else:
            time2 = (int(time2_str.split(',')[0]), int(time2_str.split(',')[1]))
        
        return time1, time2, multiple, w_time
    else:
        if ',' not in inp_str:
            h_out, m_out = int(inp_str), 0
        else:
            h_out, m_out = (int(inp_str.split(',')[0]), int(inp_str.split(',')[1]))
        return h_out, m_out, multiple, w_time


def add_times_in_list(time_list):
    """Add all times in list together"""
    h_sum = 0
    m_sum = 0
    
    for i in time_list:
        h_sum += i[0]
        
        if m_sum + i[1] > 59:
            h_sum += 1
            m_sum = (m_sum + i[1]) - 60
        elif m_sum + i[1] <= 59:
            m_sum += i[1]
    
    return h_sum, m_sum


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
    
    minutes_by_4 = ((h_in * 60) + m_in) // 4
    h_out = minutes_by_4 // 60
    m_out = minutes_by_4 % 60
    
    return h_out, m_out


def time_report():
    """Calculate total time for individual time report
    
    Legit commands:
    'q' exits input mode for time report and prints the sum of hours.
    'del' and '/del' deletes the last input for time and wait time.
    '8,0-9,0' start and stop times. Here the result is 1:00 hour.
    '3*8,0-9,0' same as above but multiplied by 3.
    '/8,0-9,0' or '/3*8,0-9,0' puts the result in the special category
    wait time.
    '8,30', '3*8,30', '/8,30' and so on also work.
    '8-12', '/2*8' for hour only."""
    times_to_add = []
    wait_times_to_add = []
    
    print('\nInputformat ("q" för att sluta/summera): hh,mm-hh,mm\n')
    
    while True:
    
        begin_end_h = input('tid arbetspass: ')
        
        if begin_end_h == 'q':
            break
        
        if begin_end_h == 'del' and times_to_add:
            print('-Arbetstid {}:{:02} raderad.'.format(*times_to_add.pop()))
            continue
        elif begin_end_h == '/del' and wait_times_to_add:
            print('-Väntetid {}:{:02} raderad.'.format(*wait_times_to_add.pop()))
            continue
        elif begin_end_h == 'del':
            print('-Det finns inget att radera!')
            continue
        
        if '-' not in begin_end_h:
            hours, mins, multiple, w_time = format_input(begin_end_h, span=False)
            
            if multiple > 1:
                hours, mins = multiply_time(hours, mins, multiple)
            
            if not w_time:
                times_to_add.append((hours, mins))
                print('{}:{:02}'.format(hours, mins))
            elif w_time:
                wait_times_to_add.append((hours, mins))
                print('{}:{:02} (väntetid)'.format(hours, mins))
        
        else:
            *timespan_tuple, w_time = format_input(begin_end_h)
            if not w_time:
                times_to_add.append(timespan_to_hours(*timespan_tuple))
                print('{}:{:02}'.format(*timespan_to_hours(*timespan_tuple)))
            elif w_time:
                wait_times_to_add.append(timespan_to_hours(*timespan_tuple))
                print('{}:{:02} (väntetid)'.format(*timespan_to_hours(*timespan_tuple)))
        
    
    h_sum, m_sum = add_times_in_list(times_to_add)
    wait_h_sum, wait_m_sum = add_times_in_list(wait_times_to_add)
    
    print('\n--Summa arbetstid: {}:{:02}\n'.format(h_sum, m_sum))
    print('--Summa väntetid: {}:{:02}'.format(wait_h_sum, wait_m_sum))
    print('_' * 24)
    return (h_sum, m_sum), (wait_h_sum, wait_m_sum)


def number_of_reports(care_receiver, care_receiver_wt):
    """Give amount of time reports
    
    Counts all time reports that doesn't have
    zeroed tuples, (0, 0), in both lists"""
    reports = 0
    
    for i in range(len(care_receiver)):
        if care_receiver[i] == (0,0) and \
           care_receiver_wt[i] == (0,0):
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
            times_to_add.append((int(hours), int(mins)))
            
            print('{}:{:02}'.format(int(hours), int(mins)))
        else:
            hours = int(time)
            times_to_add.append((hours, 0))
            
            print('{}:00'.format(hours))
    
    h_sum, m_sum = add_times_in_list(times_to_add)
    
    print('\n--Summa timmar: {}:{:02}\n'.format(h_sum, m_sum))
    print('_' * 24)


care_receiver = []
care_receiver_wait_time = []

while True:
    print('\n(1) Lägg till en tidsredovisning')
    print('(2) Avsluta/räkna ihop total arbetad tid hos brukare')
    print('(3) Addera tider fristående')
    print('(4) Radera sista inlagda tidsredovisningen')
    choice = input(': ')
    
    if choice == '1':
        times, wait_times = time_report()
        care_receiver.append(times)
        care_receiver_wait_time.append(wait_times)
        continue
    elif choice == '2':
        h_total, m_total = add_times_in_list(care_receiver)
        
        wait_h_total, wait_m_total = \
            add_times_in_list(care_receiver_wait_time)
            
        by_4_wait_h_total, by_4_wait_m_total = \
            time_by_4(wait_h_total, wait_m_total)
            
        h_final, m_final = add_times_in_list([(h_total, m_total),\
            (by_4_wait_h_total, by_4_wait_m_total)])
            
        reports = number_of_reports(care_receiver, care_receiver_wait_time)
        
        print('\n--Total arbetstid: {}:{:02}'.format(h_total, m_total))
        print('--Total väntetid (1/4): {}:{:02} ({}:{:02})'.format(wait_h_total, wait_m_total, by_4_wait_h_total, by_4_wait_m_total))
        print('--Summa total: {}:{:02}'.format(h_final, m_final))
        print('--Antal tidsredovisningar: {}'.format(reports))
        print('huvudlistan: ', care_receiver)
        print('väntelistan: ', care_receiver_wait_time)
        break
    elif choice == '3':
        add_hours()
    elif choice == '4' and care_receiver:
        print('\n-Tidsredovisning med arbetstid {}:{:02}'.format(*care_receiver.pop()), end=' ')
        print('och väntetid {}:{:02} raderad!'.format(*care_receiver_wait_time.pop()))
    elif choice == '4':
        print('\n-Det finns inga tidsredovisningar inlagda!')    
    else:
        print('\nOgiltigt val! Försök igen.\n')
