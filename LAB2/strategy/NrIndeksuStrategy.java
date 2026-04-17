package com.validation.strategy;

import java.lang.reflect.Field;
import java.util.Optional;
import com.validation.annotation.NrIndeksu;
import com.validation.annotation.ValidationFor;

@ValidationFor(NrIndeksu.class)
public class NrIndeksuStrategy implements ValidationStrategy {
    @Override
    public Optional<String> validate(Field field, Object value) {
        if (field.isAnnotationPresent(NrIndeksu.class) && value instanceof String) {
            String nr = (String) value;
            if (!nr.matches("\\d{8}")) { // Sprawdzenie czy to 8 cyfr
                NrIndeksu ann = field.getAnnotation(NrIndeksu.class);
                return Optional.of(String.format("Pole %s: %s", field.getName(), ann.message()));
            }
        }
        return Optional.empty();
    }
}