using System;
using System.Collections.Generic;
using System.Linq;

public class Patient
{
    public int Id { get; set; }
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public DateTime DateOfBirth { get; set; }
}

public class ContactInformation
{
    public int Id { get; set; }
    public int PatientId { get; set; }
    public string ContactMethod { get; set; }
    public string ContactString { get; set; }
    public bool IsPrimary { get; set; }
}

class Program
{
    static void Main(string[] args)
    {
        // Створюємо декілька прикладових об'єктів пацієнтів
        List<Patient> patients = new List<Patient>
        {
            new Patient { Id = 1, FirstName = "John", LastName = "Doe", DateOfBirth = new DateTime(1980, 5, 15) },
            new Patient { Id = 2, FirstName = "Jane", LastName = "Smith", DateOfBirth = new DateTime(1975, 10, 25) },
            new Patient { Id = 3, FirstName = "Alice", LastName = "Johnson", DateOfBirth = new DateTime(1990, 8, 5) }
        };

        // Створюємо декілька прикладових об'єктів контактної інформації
        List<ContactInformation> contactInfos = new List<ContactInformation>
        {
            new ContactInformation { Id = 1, PatientId = 1, ContactMethod = "Phone", ContactString = "123-456-7890", IsPrimary = true },
            new ContactInformation { Id = 2, PatientId = 1, ContactMethod = "Email", ContactString = "john.doe@example.com", IsPrimary = false },
            new ContactInformation { Id = 3, PatientId = 2, ContactMethod = "Phone", ContactString = "987-654-3210", IsPrimary = true }
        };

        // Ваші LINQ-запити тут

        // а) усіх пацієнтів та їх контактну інформацію
        var queryA = from patient in patients
                     join contactInfo in contactInfos on patient.Id equals contactInfo.PatientId into patientContactInfos
                     from patientContactInfo in patientContactInfos.DefaultIfEmpty()
                     select new { Patient = patient, ContactInformation = patientContactInfo };

        // б) тих пацієнтів, які не мають контактної інформації.
        var queryB = from patient in patients
                     join contactInfo in contactInfos on patient.Id equals contactInfo.PatientId into patientContactInfos
                     from patientContactInfo in patientContactInfos.DefaultIfEmpty()
                     where patientContactInfo == null
                     select patient;

        // Виведення результатів
        Console.WriteLine("Усі пацієнти та їх контактна інформація:");
        foreach (var item in queryA)
        {
            Console.WriteLine($"Patient: {item.Patient.FirstName} {item.Patient.LastName}, Contact: {item.ContactInformation?.ContactString ?? "No contact information"}");
        }

        Console.WriteLine("\nПацієнти, які не мають контактної інформації:");
        foreach (var patient in queryB)
        {
            Console.WriteLine($"Patient: {patient.FirstName} {patient.LastName}");
        }
    }
}


