import React from "react";

export interface FAQ {
  question: string;
  answer: React.ReactElement;
  contexts: string[];
  category?: string;
}
