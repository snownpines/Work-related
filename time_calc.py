def convert_h(begin_end_input):
    """Convert start and end times to time span"""
    begin = [0,0]
    end = [0,0]
    
    h_out = 0
    m_out = 0
    
    begin[0], begin[1], end[0], end[1] = format_input(begin_end_input)
    
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

def format_input(str_inp):
    """Format input for processing"""
    time1, time2 = str_inp.split('-')
    h1, m1 = int(time1.split(',')[0]), int(time1.split(',')[1])
    h2, m2 = int(time2.split(',')[0]), int(time2.split(',')[1])
    
    return h1, m1, h2, m2

times_to_add = []

print('\nInputformat: hh,mm-hh,mm\n')

while True:

    begin_end_h = input('start och stopp-tid: ')
    
    if begin_end_h == 'q':
        break
    
    times_to_add.append(convert_h(begin_end_h))
    print('{}:{:02}'.format(*convert_h(begin_end_h)), )

h_sum = 0
m_sum = 0
   
for i in times_to_add:
    h_sum += i[0]
    
    if m_sum + i[1] > 59:
        h_sum += 1
        m_sum = (m_sum + i[1]) - 60
    elif m_sum + i[1] <= 59:
        m_sum += i[1]

print('\nSumma: {}:{}\n'.format(h_sum, m_sum))
