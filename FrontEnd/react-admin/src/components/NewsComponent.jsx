import {Box, CardContent, CardMedia, Card, Link, Typography, useTheme} from "@mui/material";
import React from "react";
import SkipPreviousIcon from '@mui/icons-material/SkipPrevious';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import SkipNextIcon from '@mui/icons-material/SkipNext';
import {tokens} from "../theme";
import TickerChangeComponent from "./TickerChangeComponent";

const NewsComponent = ({news}) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    return (
        <Card sx={{ display: 'flex' }}>
            <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                <CardMedia component="img" style={{ width: 250,  height:200}} image={news.image} alt="Live from space album cover"/>
                <TickerChangeComponent ticker={news.ticker} change={news.change}/>
            </Box>
            <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                <CardContent>
                    <Link href={news.url} variant="h5" underline="hover" rel="noopener noreferrer" target="_blank" color={colors.grey[100]}>{news.title}</Link>
                    <Box sx={{ display: 'flex', flexDirection: 'row', justifyContent: "space-between" }}>
                        <Typography variant="subtitle1" color="text.secondary">{news.site}</Typography>
                        <Typography variant="subtitle1" color="text.secondary">{news.date}</Typography>
                    </Box>
                </CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent:"center", pl: 1, pb: 1}}>
                    <Typography variant="h6">{news.text}</Typography>
                </Box>
            </Box>
        </Card>
    );
};

export default NewsComponent;
