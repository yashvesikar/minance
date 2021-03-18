from minance.mock_account import MockAccount


def main(sandbox=True):
    A = MockAccount(sandbox=sandbox, testing=False)

    A.buy(1, 'MSFT')
    A.buy(3, 'MSFT')
    A.sell(2, 'MSFT')
    A.buy(1, 'MSFT')
    A.buy(3, 'MSFT')
    A.sell(2, 'MSFT')
    A.buy(1, 'MSFT')
    A.buy(3, 'MSFT')
    A.sell(2, 'MSFT')
    A.buy(1, 'MSFT')
    A.buy(3, 'MSFT')
    A.sell(2, 'MSFT')
    print(A.value())

if __name__ == "__main__":
    main()
