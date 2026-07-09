#include <iostream>
using namespace std;


void InsertionSort(int arr[], size_t n) {
    for (size_t i = 1; i < n; i++) {
        int a = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > a) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = a;
    }
}


int main()
{
    size_t n;
    cout << "Enter size of array: "; cin >> n;
    int* arr = new int[n];
    cout << "Enter "<< n <<" numbers separated by space: ";
    for (size_t i = 0; i < n; i++) {
        cin >> arr[i];
    }
    cout << "Your array:" << endl;
    for (size_t i = 0; i < n; i++) {
        cout << arr[i] << " ";
    }
    
    cout << endl << "Sorted array: " << endl;
    InsertionSort(arr, n);
    for (int i = 0; i < n; i++) {
        cout << arr[i] << " ";
    }

	return 0;
}