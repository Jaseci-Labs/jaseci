import from mtllm.llms.base { BaseLLM }
import:py from PIL { Image }
import torch;
import from transformers { AutoModelForCausalLM, AutoProcessor }

glob PROMPT_TEMPLATE:str= """
[Information]
{information}

[Output Information]
{output_information}

[Type Explanations]
{type_explanations}

[Action]
{action}
""";

obj Florence :BaseLLM: {
    with entry{
        MTLLM_PROMPT = PROMPT_TEMPLATE;
    }
    can init(model_id: str) {
        self.verbose = True;
        self.max_tries = 0;
        self.type_check = False;
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            trust_remote_code=True, torch_dtype='auto'
        ).eval().cuda();
        self.processor = AutoProcessor.from_pretrained(
            model_id,
            trust_remote_code=True
        );
    }

    can __infer__(meaning: str, image: Image, **kwargs: tuple) -> str {
        can run_example(task_prompt: str, image: Image) -> str {
            prompt = task_prompt;
            inputs = self.processor(
                text=prompt,
                images=image,
                return_tensors="pt"
            ).to(
                'cuda',
                torch.float16
            );
            generated_ids = self.model.generate(
                input_ids=inputs["input_ids"].cuda(),
                pixel_values=inputs["pixel_values"].cuda(),
                max_new_tokens=1024,
                early_stopping=False,
                do_sample=False,
                num_beams=3,

            );
            generated_text = self.processor.batch_decode(
                generated_ids,
                skip_special_tokens=False
            )[0];
            parsed_answer = self.processor.post_process_generation(
                generated_text,
                task=task_prompt, image_size=(image.width, image.height)
            );

            return parsed_answer;
        }

        result = run_example('<MORE_DETAILED_CAPTION>', image=image);
        return str(next(iter(result.values())));
    }

    can __call__(meaning: str, media: list, **kwargs: tuple) {
        if self.verbose{
            print(f'MEANING_IN:\n{meaning}');
            print('MEDIA:\n',media);
        }
        image = media[0].value;
        return self.__infer__(meaning, image, **kwargs);
    }
}

glob llm = Florence('microsoft/Florence-2-base');

enum DamageType {
    NoDamage,
    MinorDamage,
    MajorDamage,
    Destroyed
}

can ""
predict_vehicle_damage(img: Image) -> DamageType by llm(is_custom=True);

with entry {
    img = 'car_scratch.jpg';
    image = Image.open(img);
    print(predict_vehicle_damage(image));
}
