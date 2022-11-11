import { NumberField } from "@adobe/react-spectrum";
import { Controller } from "react-hook-form";
import type { Control, FieldValues } from "react-hook-form";
import { ComponentProps } from "react";

function FormNumberField({
  name,
  control,
  ...props
}: { control: Control<FieldValues, any>; name: string } & ComponentProps<
  typeof NumberField
>) {
  return (
    <Controller
      name={name}
      control={control}
      render={({ field, fieldState }) => (
        <NumberField
          {...props}
          validationState={
            fieldState.error
              ? "invalid"
              : fieldState.isDirty || fieldState.isTouched
              ? "valid"
              : undefined
          }
          value={field.value}
          onChange={(e) => field.onChange(e)}
        ></NumberField>
      )}
    ></Controller>
  );
}

export default FormNumberField;
