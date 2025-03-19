import type { Preview } from "@storybook/react";

import "/src/views/styles/global/colors.css";
import "/src/views/styles/global/root.css";
import "/.storybook/storybook.css";

const preview: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
  },
};

export default preview;
