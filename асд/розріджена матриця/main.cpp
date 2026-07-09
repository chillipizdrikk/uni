#include <iostream>
#include <stack>
#include <vector>
#include <algorithm>
#include <string>
#include <cmath>  /* for std::abs(double) */
using namespace std;

inline bool isEqual(double x, double y)
{
    const double epsilon = 1e-5/* some small number such as 1e-5 */;
    return std::abs(x - y) <= epsilon * std::abs(x);
    // see Knuth section 4.2.2 pages 217-218
}

struct Element {
    size_t Row;
    size_t Col;
    double Value;
    Element* left;
    Element* up;
    Element() {
        left = this;
        up = this;
        Row = -1;
        Col = -1;
    }
    Element(size_t row, size_t col, double value) :
        Element() {
        Row = row;
        Col = col;
        Value = value;
    };
};

class SparceMatrix {
    size_t rows;
    size_t cols;
    vector<Element> rowsHeaders;
    vector<Element> colsHeaders;

public:
    SparceMatrix(size_t rows, size_t cols) {
        this->rows = rows;
        this->cols = cols;
        rowsHeaders.resize(rows);
        colsHeaders.resize(cols);
    }
    SparceMatrix(const SparceMatrix& other) {
        *this = other;
    }
    ~SparceMatrix() {
        ClearContainers();
    }

    void ClearContainers() {
        for (size_t i = 0; i < rows; i++) {
            Element* iterator = rowsHeaders[i].left;
            while (iterator != &rowsHeaders[i]) {
                Element* elemToDel = iterator;
                iterator = iterator->left;
                delete elemToDel;
            }
        }
        rowsHeaders.resize(0);
        colsHeaders.resize(0);
    }

    SparceMatrix& operator =(const SparceMatrix& other) {
        ClearContainers();
        rows = other.rows;
        cols = other.cols;
        rowsHeaders.resize(rows);
        colsHeaders.resize(cols);

        for (size_t i = 0; i < rows; i++)
        {
            /*
            TODO: make more efficient
            Element* iterator = other.rowsHeaders[i].left;
            while (iterator != &other.rowsHeaders[i]) {
                Element* elemToDel = iterator;
                iterator = iterator->left;
                delete elemToDel;
            }*/

            for (size_t j = 0; j < cols; j++)
            {
                //other.GetValue(i, j)

                SetValue(i, j, other.GetValue(i, j));
            }
        }
        return *this;
    }

    const Element* getPrevByRow(size_t i, size_t j) const {
        const Element* result = &rowsHeaders[i];
        Element* iterator = rowsHeaders[i].left;
        while (iterator != &rowsHeaders[i]) {
            if (j >= iterator->Col) {
                break;
            }
            result = iterator;
            iterator = iterator->left;
        }
        return result;

    }

    const Element* getPrevByCol(size_t i, size_t j) const {
        const Element* result = &colsHeaders[j];
        Element* iterator = colsHeaders[j].left;
        while (iterator != &colsHeaders[j]) {
            if (i >= iterator->Row) {
                break;
            }
            result = iterator;
            iterator = iterator->up;
        }
        return result;
    }




    void SetValue(size_t i, size_t j, double value) {
        Element* prevByCol = (Element*)getPrevByCol(i, j);
        Element* prevByRow = (Element*)getPrevByRow(i, j);
        //елемент вже є
        if (prevByCol->up->Row == i && prevByCol->up->Col == j) {
            prevByCol->up->Value = value;
            if (isEqual(value, 0)) {
                Element* elemToDelete = prevByCol->up;

                prevByCol->up = elemToDelete->up;
                prevByRow->left = elemToDelete->left;
                delete elemToDelete;
            }
        }
        else {
            //елемента нема
            if (!isEqual(value, 0)) {
                Element* newElement = new Element(i, j, value);

                newElement->left = prevByRow->left;
                prevByRow->left = newElement;

                newElement->up = prevByCol->up;
                prevByCol->up = newElement;
            }
        }

    }

    double GetValue(size_t i, size_t j) const {
        double result = 0;
        Element* prevByCol = (Element*)getPrevByCol(i, j);
        //елемент вже є
        if (prevByCol->up->Row == i && prevByCol->up->Col == j) {
            result = prevByCol->up->Value;
        }

        return result;
    }

    SparceMatrix AddMatrix(SparceMatrix& other) {
        if (this->cols != other.cols || this->rows != other.rows) {
            throw "cannot add different sized matrices";
        };
        SparceMatrix result(rows, cols);
        for (size_t i = 0; i < rows; i++) {
            for (size_t j = 0; j < cols; j++) {
                double sum;
                sum = this->GetValue(i, j) + other.GetValue(i, j);
                result.SetValue(i, j, sum);
            }
        }
        return result;
    }

    void print() {
        // print the matrix
        for (size_t i = 0; i < rows; i++) {
            for (size_t j = 0; j < cols; j++) {
                cout << GetValue(i, j) << " ";
            }
            cout << endl;
        }
    }

    SparceMatrix transpose() {
        // compute the transpose of the matrix
        SparceMatrix transposed(cols, rows);
        for (size_t i = 0; i < rows; i++) {
            for (size_t j = 0; j < cols; j++) {
                transposed.SetValue(j, i, GetValue(i, j));
            }
        }
        return transposed;
    }

    SparceMatrix MultiplyMatrix(SparceMatrix& other) {
        if (this->cols != other.rows) {
            throw "cannot add different sized matrices";
        };
        SparceMatrix result(this->rows, other.cols);
        for (size_t i = 0; i < this->rows; i++) {
            for (size_t j = 0; j < other.cols; j++) {
                double scalarProduct = 0;
                for (size_t k = 0; k < this->cols; k++)
                {
                    scalarProduct +=
                        this->GetValue(i, k) * other.GetValue(k, j);
                }

                result.SetValue(i, j, scalarProduct);
            }
        }
        return result;
    }

};

/*TEST_CASE*/

int main()
{
    SparceMatrix matr1(3, 4);
    /*  0 0 1 0
    *   0 2 0 0
    *   0 2 1 0
    */
    matr1.SetValue(0, 2, 1);
    matr1.SetValue(1, 1, 2);
    matr1.SetValue(2, 3, 0);

    SparceMatrix matr2(matr1);
    /*  0 0 1 0
   *    4 2 0 0
   *    0 0 3 0
   */
    matr2.SetValue(1, 0, 4);
    SparceMatrix matrAdd(matr1.AddMatrix(matr2));

    cout << (matrAdd.GetValue(1, 0) == 4) << endl;
    cout << (matrAdd.GetValue(1, 2) == 8) << endl;

    SparceMatrix matr3(3, 4);
    /*  0 1 0 0
   *    0 0 2 0
   *    0 0 0 3
   */
    matr3.SetValue(0, 1, 1);
    matr3.SetValue(1, 2, 2);
    matr3.SetValue(2, 3, 3);


    SparceMatrix matr4(2, 3);
    matr4.SetValue(0, 0, 1);
    matr4.SetValue(0, 1, 2);
    matr4.SetValue(0, 2, 3);

    SparceMatrix matr5(3, 2);
    matr5.SetValue(1, 0, 3);
    matr5.SetValue(1, 1, -1);
    matr5.SetValue(2, 0, 4);

    SparceMatrix matrMul(1, 1);
    matrMul = matr4.MultiplyMatrix(matr5);
    cout << (matrMul.GetValue(0, 0) == 16) << endl;
    cout << (matrMul.GetValue(0, 1) == -2) << endl;
    cout << (matrMul.GetValue(1, 1) == 0) << endl;

    return 1;
}