from prettytable import PrettyTable
import matplotlib.pyplot as plt
import numpy as np
import decimal


class Helper:
    """ Helper class for printing and plotting of loan schedules.
    """
    @staticmethod
    def display(value, digits=2):
        """ Return a displayable value with a specified number of digits.
        :param value: value to display
        :param digits: number of digits right of the decimal place
        :return: formatted displayable value
        """
        temp = str(decimal.Decimal(str(value) + '0' * digits))
        return temp[:temp.find('.') + digits + 1]

    @staticmethod
    def plot(loan):
        payment_number, applied_principal, applied_interest, end_principal = [], [], [], []

        # iterate over the loan schedule
        #
        for pay in loan.schedule.values():
            payment_number.append(pay[0])
            applied_principal.append(pay[4])
            applied_interest.append(pay[5])
            end_principal.append(pay[6])

        ind = np.arange(len(payment_number))
        width = 0.35
        p1 = plt.bar(ind, applied_principal, width)
        p2 = plt.bar(ind, applied_interest, width, bottom=applied_principal)

        plt.ylabel('USD')
        plt.title('Schedule')
        plt.xticks(np.arange(0, max(payment_number), 12))
        plt.yticks(np.arange(0, max(applied_principal + applied_interest), 500))
        plt.legend((p1[0], p2[0]), ('Principal', 'Interest'), loc='lower right')
        plt.show()

    @staticmethod
    def print(loan):
        x = PrettyTable()
        x.field_names = ['Payment Number', 'Begin Principal', 'Payment', 'Extra Payment',
                         'Applied Principal', 'Applied Interest', 'End Principal']
        for field_name in x.field_names:
            x.align[field_name] = "r"
        for pay in loan.schedule.values():
            x.add_row([pay[0],
                       Helper.display(pay[1]),
                       Helper.display(pay[2]),
                       Helper.display(pay[3]),
                       Helper.display(pay[4]),
                       Helper.display(pay[5]),
                       Helper.display(pay[6])])
        print(x)

