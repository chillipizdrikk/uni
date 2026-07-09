#include <iostream>
using namespace std;


int MaxVal(int arr[], int size)//знаходження максимального елемента
{
    int max = arr[0];
    for (int i = 1; i < size; i++)
    {
        if (arr[i] > max)
        {
            max = arr[i];
        }
    }
    return max;
}

void CountingSort(int arr[], int size, int dig)
{
    int out[10];
    int calc[10] = { 0 };

    for (int i = 0; i < size; i++)//цикл для розподілення елементів масиву за розрядами
    {
        calc[(arr[i] / dig) % 10]++;
    }

    for (int i = 1; i < 10; i++)//цикл для підрахунку кількості елементів в кожному розряді
    {
        calc[i] += calc[i - 1];
    }

    for (int i = size - 1; i >= 0; i--)//цикл для перенесення елементів в масив arr відсортованих у зворотному порядку
    {
        out[calc[(arr[i] / dig) % 10] - 1] = arr[i];
        calc[(arr[i] / dig) % 10]--;
    }

    for (int i = 0; i < size; i++)//цикл для копіювання відсортованого масиву в arr
    {
        arr[i] = out[i];
    }
}

void RadixSort(int arr[], int size)
{
    int r = MaxVal(arr, size);
    for (int dig = 1; r / dig > 0; dig *= 10)
    {
        CountingSort(arr, size, dig);
    }
}


int main()
{
    size_t n;
    cout << "Enter size of array: "; cin >> n;
    int* arr = new int[n];
    cout << "Enter " << n << " numbers separated by space: ";
    for (size_t i = 0; i < n; i++) {
        cin >> arr[i];
    }
    cout << "Your array:" << endl;
    for (size_t i = 0; i < n; i++) {
        cout << arr[i] << " ";
    }

    cout << endl << "Sorted array: " << endl;
    RadixSort(arr, n);
    for (int i = 0; i < n; i++) {
        cout << arr[i] << " ";
    }

    return 0;
}



//#include <vector>
//#include <algorithm>
//
//using namespace std;
//
//void RadixSort(vector<int>& arr) {
//    int max_val = *max_element(arr.begin(), arr.end());
//    for (int exp = 1; max_val / exp > 0; exp *= 10) {
//        vector <int> out(arr.size());
//        vector <int> calc(10, 0);
//        for (int i = 0; i < arr.size(); i++) {
//            calc[(arr[i] / exp) % 10]++;
//        }
//        for (int i = 1; i < 10; i++) {
//            calc[i] += calc[i - 1];
//        }
//        for (int i = arr.size() - 1; i >= 0; i--) {
//            out[calc[(arr[i] / exp) % 10] - 1] = arr[i];
//            calc[(arr[i] / exp) % 10]--;
//        }
//        for (int i = 0; i < arr.size(); i++) {
//            arr[i] = out[i];
//        }
//    }
//}
//
//int main() {
//    vector <int> arr = { 579, 25, 43, 10, 682, 41, 4, 57, 33 };
//
//    RadixSort(arr);
//
//    cout << "Sorted array: ";
//    for (int i = 0; i < arr.size(); i++) {
//        cout << arr[i] << " ";
//    }
//    cout << endl;
//
//    return 0;
//}