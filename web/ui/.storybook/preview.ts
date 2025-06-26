import type { Preview } from "@storybook/react";
import "primeicons/primeicons.css";
import "primereact/resources/themes/saga-blue/theme.css";
import "primereact/resources/primereact.min.css";

import "/src/views/styles/global/colors.css";
import "/src/views/styles/global/root.css";
import "/src/views/styles/global/zIndex.css";
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
