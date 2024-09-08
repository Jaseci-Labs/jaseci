export const getGraphWebviewContent = (graphSvg: string) => {
  return `
	<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
<p>Hello</p>
  ${graphSvg}
</body>
</html>
	`;
};
