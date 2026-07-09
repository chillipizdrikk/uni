using System;

class task2
{
    // Коваріантний делегат, оскільки тип результату методу GetDerived() 
    // (типу DerivedClass) є похідним від типу результату делегата (типу BaseClass)
    delegate BaseClass BaseClassGetter();

    // Контраваріантний делегат, оскільки параметр методу HandleBaseClass() 
    // (типу BaseClass) є базовим для типу параметра делегата (типу DerivedClass)
    delegate void DerivedClassHandler(DerivedClass derived);

    static DerivedClass GetDerived()
    {
        return new DerivedClass();
    }

    static void HandleBaseClass(BaseClass baseClass)
    {
        Console.WriteLine($"Обробляє {baseClass.GetType().Name}");
    }

    static void Main(string[] args)
    {
        // Коваріантність: прив'язуємо метод GetDerived() до коваріантного делегата BaseClassGetter
        BaseClassGetter baseClassGetter = GetDerived;
        BaseClass baseClass = baseClassGetter();
        Console.WriteLine(baseClass.GetType().Name); // Виведе "DerivedClass"

        // Контраваріантність: прив'язуємо метод HandleBaseClass() до контраваріантного делегата DerivedClassHandler
        DerivedClassHandler derivedHandler = HandleBaseClass;
        DerivedClass derived = new DerivedClass();
        derivedHandler(derived); // Виведе "Обробка DerivedClass"
    }
}

class BaseClass { }
class DerivedClass : BaseClass { }
