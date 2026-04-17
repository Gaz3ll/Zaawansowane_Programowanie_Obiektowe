package com.validation.strategy;

import java.lang.reflect.Field;
import java.util.Optional;
import com.validation.annotation.Size;
import com.validation.annotation.ValidationFor;

@ValidationFor(Size.class)
public class SizeStrategy implements ValidationStrategy {
    @Override
    public Optional<String> validate(Field field, Object value) {
        if (field.isAnnotationPresent(Size.class) && value instanceof String) {
            Size ann = field.getAnnotation(Size.class);
            String str = (String) value;
            if (str.length() < ann.min() || str.length() > ann.max()) {
                String msg = ann.message()
                        .replace("{min}", String.valueOf(ann.min()))
                        .replace("{max}", String.valueOf(ann.max()));
                return Optional.of(String.format("Pole %s: %s", field.getName(), msg));
            }
        }
        return Optional.empty();
    }
}