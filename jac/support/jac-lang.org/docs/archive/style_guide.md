## Jac Code Style Guide with Before and After Examples

### Detailed Guidelines and Examples

#### 1. **Comments**
   - **Explanation**: Comments should be clear and concise, providing meaningful information about the code. They should be preceded by a space after the `#` symbol for readability.
   - **Before**:
     ```jac
     can say_hello with entry abs;# data spatial ability declared
     ```
   - **After**:
     ```jac
     can say_hello with entry abs; # data spatial ability declared
     ```

#### 2. **Import Statements**
   - **Explanation**: Organize import statements for clarity. Group and order imports logically, starting with standard library imports, followed by third-party imports, and then local module imports. Separate different types of imports (like Python imports and Jac imports) for better readability. End each import statement with a semicolon. Use comments to explain the purpose of imports or includes when necessary.
   - **Before**:
     ```jac
     import:py random;
     import:py from math, sqrt as square_root;  # list of as clauses comes at end
     import:py datetime as dt;
     include:jac defs.mod_defs;  # includes are useful when bringing definitions into scope
     import:jac from defs.main_defs, jactastic;
     ```
   - **After**:
     ```jac
     import:py random;
     import:py from math, sqrt as square_root;  # list of as clauses comes at end
     import:py datetime as dt;

     include:jac defs.mod_defs;  # includes are useful when bringing definitions into scope
     import:jac from defs.main_defs, jactastic;


#### 3. **Object and Method Definitions**
   - **Explanation**: Object and method definitions should be clear with consistent indentation. Use braces to define the scope of objects and methods.
   - **Before**:
     ```jac
     obj Game{can init(attempts:int){...}}
     ```
   - **After**:
     ```jac
     obj Game {
         can init(attempts: int) {
             ...
         }
     }
     ```

#### 4. **Spacing and Indentation**
   - **Explanation**: Consistent spacing and indentation are crucial for readability. Use spaces around operators and after commas.
   - **Before**:
     ```jac
     obj Game{can init(attempts:int){self.attempts=attempts;}}
     ```
   - **After**:
     ```jac
     obj Game {
         can init(attempts: int) {
             self.attempts = attempts;
         }
     }
     ```

#### 5. **Variable Assignments**
   - **Explanation**: In variable assignments, use spaces around the `=` operator for clarity.
   - **Before**:
     ```jac
     self.attempts=attempts;
     ```
   - **After**:
     ```jac
     self.attempts = attempts;
     ```

#### 6. **Conditional and Loop Statements**
   - **Explanation**: For conditional and loop statements, use a space after the statement keyword and enclose conditions in parentheses.
   - **Before**:
     ```jac
     if guess.isdigit(){...}
     ```
   - **After**:
     ```jac
     if guess.isdigit() {
         ...
     }
     ```

#### 7. **String Formatting**
   - **Explanation**: Prefer using formatted string literals for dynamic string creation, as they are more readable and concise.
   - **Before**:
     ```jac
     print("You have "+self.attempts+" attempts left.");
     ```
   - **After**:
     ```jac
     print(f"You have {self.attempts} attempts left.");
     ```

#### 8. **Line Breaks and Blank Lines**
   - **Explanation**: Use line breaks and blank lines to separate logical sections of code, enhancing readability.
   - **Before**:
     ```jac
     self.won=False;can play(){...}
     ```
   - **After**:
     ```jac
     self.won = False;

     can play() {
         ...
     }
     ```

#### 9. **Special Constructs**
   - **Explanation**: Special constructs like `with entry` should be formatted with clear indentation and spacing for each statement.
   - **Before**:
     ```jac
     with entry{game=GuessTheNumberGame();game.play();}
     ```
   - **After**:
     ```jac
     with entry {
         game = GuessTheNumberGame();
         game.play();
     }
     ```

#### 10. **Error Handling**
[comment]: <> (Todo: Add explanation)


#### 11. **Function Calls**
   - **Explanation**: When calling functions, use consistent spacing around arguments.
   - **Before**:
     ```jac
     doSomething(arg1,arg2);
     ```
   - **After**:
     ```jac
     doSomething(arg1, arg2);
     ```

#### 12. **Complex Expressions**
  [comment]: <> (need to implement)
   - **Explanation**: Break down complex expressions into multiple lines for better readability.
   - **Before**:
     ```jac
     if condition1 && condition2 || condition3 { ... }
     ```
   - **After**:
     ```jac
     if (condition1 && condition2) ||
        condition3 {
         ...
     }
     ```

---