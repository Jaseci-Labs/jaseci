import { Controller } from "react-hook-form";
import type { Control, FieldValues } from "react-hook-form";
import { ComponentProps } from "react";
import { TextInput } from "@mantine/core";

function FormTextField({
  name,
  control,
  ...props
}: { control: Control<FieldValues, any>; name: string } & ComponentProps<
  typeof TextInput
>) {
  return (
    <Controller
      name={name}
      control={control}
      render={({ field, fieldState }) => (
        <TextInput
          {...props}
          error={fieldState.error?.message}
          value={field.value}
          onChange={(e) => field.onChange(e)}
        ></TextInput>
      )}
    ></Controller>
  );
}

export default FormTextField;
