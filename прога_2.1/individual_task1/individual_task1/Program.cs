/*Добрий день, перепрошую за код, він має простий функціонал і не надто наповнений, але коротко розкажу: 
 * В мене є такі класи як сонце, квітка, бджола та дівчинка. Сонце може змінювати свій стан (сходить або заходить). 
 * Квітка реагує на зміну стану сонця і залежно від типу(денна/нічна) може розпускатися і цвісти або в'янути. 
 * Бджола також реагує на зміну стану сонця(мордує квіти або летить додому).
 * Дівчинка спостерігає за квітами, коли їй цікаво(в мене вона спостерігає ввечері після роботи)*/

using System;

//Клас MySunEventArgs наслідується від EventArgs і містить властивість SunState, яка представляє стан сонця
public class MySunEventArgs : EventArgs
{
    public string SunState { get; set; }
}


public class MySun
{
    public event EventHandler<MySunEventArgs> SunStateChanged;

    public void ChangeSunState()
    {
        Console.WriteLine("Введіть стан Сонця (Сходить/Заходить):");
        string sunState = Console.ReadLine();
        OnSunStateChanged(sunState);
    }

    protected virtual void OnSunStateChanged(string sunState)
    {
        SunStateChanged?.Invoke(this, new MySunEventArgs { SunState = sunState });
    }
}

//Клас MyFlower представляє квітку, він має внутрішні змінні для збереження кількості днів до цвітіння, типу квітки та прапорця, який вказує, чи зав'яла квітка
//Метод ReactToSun обробляє подію SunStateChanged, змінюючи стан квітки відповідно до стану сонця
public class MyFlower
{
    private int _daysToBloom;
    private string _type;
    private bool _isWithered;

    public MyFlower(int daysToBloom, string type)
    {
        _daysToBloom = daysToBloom;
        _type = type;
        _isWithered = false;
    }

    public void ReactToSun(object sender, MySunEventArgs e)
    {
        if (_isWithered)
        {
            Console.WriteLine("Нова квіточка починає розпускатися");
            _isWithered = false;
            _daysToBloom = 10;
        }

        if (_daysToBloom <= 0)
        {
            Console.WriteLine("Квітка вмерла");
            _isWithered = true;
            return;
        }

        switch (e.SunState)
        {
            case "Сходить":
                if (_type == "Денна")
                {
                    Console.WriteLine("Квітка розпускається");
                    _daysToBloom--;
                }
                break;
            case "Заходить":
                if (_type == "Нічна")
                {
                    Console.WriteLine("Квітка розпускається");
                    _daysToBloom--;
                }
                break;
        }
    }
}

public class MyBee
{
    public void ReactToSun(object sender, MySunEventArgs e)
    {
        switch (e.SunState)
        {
            case "Сходить":
                Console.WriteLine("Бджола вирішує помордувати квіточки");
                break;
            case "Заходить":
                Console.WriteLine("Бджола повертається додому");
                break;
        }
    }
}


public class MyGirl
{
    private bool _isWeekend;

    public MyGirl(bool isWeekend)
    {
        _isWeekend = isWeekend;
    }

    public void ReactToSun(object sender, MySunEventArgs e)
    {
        if (_isWeekend && e.SunState == "Сходить" || !_isWeekend && e.SunState == "Заходить")
        {
            Console.WriteLine("Дівчинка прийшла з роботи і насолоджується квітником");
        }
    }
}

//Головний клас MyProgram створює об'єкти сонця, квітки, бджоли та дівчинки. запускає цикл, який протягом 30 днів змінює стан сонця
public class MyProgram
{
    public static void Main()
    {
        var sun = new MySun();
        var flower = new MyFlower(3, "Денна");
        var bee = new MyBee();
        var girl = new MyGirl(false);

        sun.SunStateChanged += flower.ReactToSun;
        sun.SunStateChanged += bee.ReactToSun;
        sun.SunStateChanged += girl.ReactToSun;

        for (var i = 0; i < 30; i++)
        {
            sun.ChangeSunState();
        }
    }
}
