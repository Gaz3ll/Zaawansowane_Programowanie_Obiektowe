package com.validation;

import com.validation.exception.ValidationException;
import com.validation.validator.Validator;

public class Main {
    public static void main(String[] args) {
        try {
            // Testowanie z błędnymi danymi
            Student student = new Student();
            student.setImie("Jo"); // Zbyt krótkie
            student.setNazwisko(null);  // Brak nazwiska
            student.setNrIndeksu("123"); // Zły format indeksu
            student.setEmail("jan.kowalski@pbs.edu.pl"); // Błędny email

            Validator.validate(student);
        } catch (ValidationException e) {
            System.out.println("Wykryto błędy walidacji:");
            System.out.println(e.getMessage());
        }
    }
}