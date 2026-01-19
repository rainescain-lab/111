export type QuizAnswers = {
  q1: string;
  q2: string;
  q3: string;
  q4: string[];
  q5: string;
};

export type ProfileVector = {
  risk: number;
  content: number;
  scale: number;
  cash: number;
  lifecycle: "short" | "mid" | "long";
};

export type ProfileResult = {
  vector: ProfileVector;
  segment: "new_seller" | "creator" | "mcn" | "ads_scaler" | "operator";
};

const clamp = (value: number) => Math.max(0, Math.min(100, value));

export function buildProfile(answers: QuizAnswers): ProfileResult {
  let risk = 50;
  let content = 50;
  let scale = 50;
  let cash = 50;
  let lifecycle: ProfileVector["lifecycle"] = "mid";

  switch (answers.q1) {
    case "A":
      risk -= 15;
      cash -= 15;
      break;
    case "B":
      risk -= 5;
      break;
    case "C":
      risk += 10;
      cash += 10;
      break;
    case "D":
      risk += 20;
      cash += 20;
      break;
    default:
      break;
  }

  switch (answers.q2) {
    case "A":
      content += 20;
      scale -= 5;
      break;
    case "B":
      content += 5;
      scale += 5;
      break;
    case "C":
      content -= 5;
      scale += 20;
      break;
    case "D":
      content -= 10;
      scale += 25;
      break;
    default:
      break;
  }

  switch (answers.q3) {
    case "A":
      risk -= 10;
      lifecycle = "long";
      break;
    case "B":
      risk += 5;
      lifecycle = "short";
      break;
    case "C":
      risk += 10;
      lifecycle = "mid";
      break;
    default:
      break;
  }

  const operations = answers.q4.length;
  risk += operations >= 3 ? 10 : operations === 2 ? 5 : 0;
  scale += operations >= 3 ? 5 : 0;

  switch (answers.q5) {
    case "A":
      lifecycle = "long";
      risk -= 5;
      break;
    case "B":
      lifecycle = "mid";
      break;
    case "C":
      lifecycle = "short";
      risk += 10;
      break;
    case "D":
      content += 10;
      break;
    default:
      break;
  }

  const vector = {
    risk: clamp(risk),
    content: clamp(content),
    scale: clamp(scale),
    cash: clamp(cash),
    lifecycle
  };

  let segment: ProfileResult["segment"] = "new_seller";
  if (scale > 70 && risk > 60) {
    segment = "ads_scaler";
  } else if (scale > 70 && content > 50) {
    segment = "mcn";
  } else if (content > 70) {
    segment = "creator";
  } else if (cash > 60 && risk > 50) {
    segment = "operator";
  }

  return { vector, segment };
}
