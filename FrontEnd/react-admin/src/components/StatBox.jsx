import React from "react";
import { Box, Typography, useTheme } from "@mui/material";
import FlexBetween from "./FlexBetween";
import {tokens} from "../theme";

const StatBox = ({ title, value, icon }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  return (
      <Box
          gridColumn="span 2"
          gridRow="span 1"
          display="flex"
          flexDirection="column"
          justifyContent="space-between"
          p="1.25rem 1rem"
          flex="1 1 100%"
          backgroundColor={colors.blueAccent[800]}
          borderRadius="0.55rem"
      >
        <FlexBetween>
          <Box>
            <Typography variant="h6" sx={{ color: colors.primary[100] }}>
              {title}
            </Typography>
            <Typography
                variant="h3"
                fontWeight="600"
                sx={{ color: theme.palette.secondary[200] }}
            >
              {value}
            </Typography>
          </Box>

          {icon}
        </FlexBetween>

      </Box>
  );
};

export default StatBox;