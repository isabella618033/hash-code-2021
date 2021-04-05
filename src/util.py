from datetime import datetime

def print_score(loss_total, score, arrived, total):
    print('loss_total: {}'.format(loss_total))
    print('Score: {}'.format(score))
    print('Arrived/Total: {} / {}'.format(arrived, total))

def log_section(msg):
    rPad = 80
    print(('{} {} '.format(datetime.now(), msg)).ljust(rPad, '='))
