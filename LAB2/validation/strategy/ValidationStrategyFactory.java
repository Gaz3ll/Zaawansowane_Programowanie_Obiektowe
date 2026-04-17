package com.validation.strategy;

import java.lang.annotation.Annotation;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import com.validation.annotation.ValidationFor;

public class ValidationStrategyFactory {
    private static final Map<Class<? extends Annotation>, ValidationStrategy> strategies = new HashMap<>();

    static {
        // Implementacja automatycznego wyszukiwania (uproszczona wersja dla zadania dodatkowego)
        // W rzeczywistym projekcie używa się bibliotek typu 'Reflections'
        ValidationStrategy[] manualStrategies = {
            new NotNullStrategy(),
            new NotEmptyStrategy(),
            new SizeStrategy(),
            new NrIndeksuStrategy(),
            new EmailStrategy()
        };

        for (ValidationStrategy strategy : manualStrategies) {
            ValidationFor vf = strategy.getClass().getAnnotation(ValidationFor.class);
            if (vf != null) {
                strategies.put(vf.value(), strategy);
            }
        }
    }

    private ValidationStrategyFactory() {}

    public static ValidationStrategy getStrategy(Annotation annotation) {
        return strategies.get(annotation.annotationType());
    }
}