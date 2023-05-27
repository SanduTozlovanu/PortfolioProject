import {useContext, useState} from "react";
import {ProSidebar, Menu, MenuItem} from "react-pro-sidebar";
import {Box, IconButton, Typography, useTheme} from "@mui/material";
import {Link} from "react-router-dom";
import "react-pro-sidebar/dist/css/styles.css";
import {tokens} from "../../theme";
import AccessibilityIcon from '@mui/icons-material/Accessibility';
import AppRegistrationIcon from '@mui/icons-material/AppRegistration';
import LoginIcon from '@mui/icons-material/Login';
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";
import NewspaperIcon from '@mui/icons-material/Newspaper';
import ReceiptLongIcon from '@mui/icons-material/ReceiptLong';
import BarChartOutlinedIcon from "@mui/icons-material/BarChartOutlined";
import PieChartOutlineOutlinedIcon from "@mui/icons-material/PieChartOutlineOutlined";
import TimelineOutlinedIcon from "@mui/icons-material/TimelineOutlined";
import MenuOutlinedIcon from "@mui/icons-material/MenuOutlined";
import QueryStatsIcon from '@mui/icons-material/QueryStats';
import WorkIcon from '@mui/icons-material/Work';
import Authcontext from "../../components/AuthContext";

const Item = ({title, to, icon, selected, setSelected}) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    return (
        <MenuItem
            active={selected === title}
            style={{
                color: colors.grey[100],
            }}
            onClick={() => setSelected(title)}
            icon={icon}
        >
            <Typography>{title}</Typography>
            <Link to={to}/>
        </MenuItem>
    );
};

function Sidebar({onToggleCollapse}) {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const { isAuthenticated, setIsAuthenticated, name, setName } = useContext(Authcontext);
    const [isCollapsed, setIsCollapsed] = useState(false);
    const [selected, setSelected] = useState("Dashboard");

    const handleCollapseToggle = () => {
        onToggleCollapse(isCollapsed);
    };

    return (
        <Box
            sx={{
                "& .pro-sidebar-inner": {
                    background: `${colors.primary[400]} !important`,
                },
                "& .pro-icon-wrapper": {
                    backgroundColor: "transparent !important",
                },
                "& .pro-inner-item": {
                    padding: "5px 35px 5px 20px !important",
                },
                "& .pro-inner-item:hover": {
                    color: "#868dfb !important",
                },
                "& .pro-menu-item.active": {
                    color: "#6870fa !important",
                },
            }}
        >
            <ProSidebar collapsed={isCollapsed} style={{position: 'fixed'}}>
                <Menu iconShape="square">
                    {/* LOGO AND MENU ICON */}
                    <MenuItem
                        onClick={() => {
                            setIsCollapsed(!isCollapsed)
                            handleCollapseToggle()

                        }}
                        icon={isCollapsed ? <MenuOutlinedIcon/> : undefined}
                        style={{
                            margin: "10px 0 20px 0",
                            color: colors.grey[100],
                        }}
                    >
                        {!isCollapsed && (
                            <Box
                                display="flex"
                                justifyContent="space-between"
                                alignItems="center"
                                ml="15px"
                            >
                                <Typography variant="h3" color={colors.grey[100]}>{isAuthenticated ? 'User' : 'Unlogged User'}
                                </Typography>
                                <IconButton onClick={() => {
                                    setIsCollapsed(!isCollapsed)
                                    handleCollapseToggle()
                                }}>
                                    <MenuOutlinedIcon/>
                                </IconButton>
                            </Box>
                        )}
                    </MenuItem>

                    {!isCollapsed && isAuthenticated && (
                        <Box mb="25px">
                            <Box textAlign="center">
                                <Typography
                                    variant="h3"
                                    color={colors.grey[100]}
                                    fontWeight="bold"
                                    sx={{m: "10px 0 0 0"}}
                                >
                                    {name}
                                </Typography>
                                <Typography variant="h5" color={colors.greenAccent[500]}>
                                    Investor
                                </Typography>
                            </Box>
                        </Box>
                    )}

                    <Box paddingLeft={isCollapsed ? undefined : "10%"}>
                        {!isAuthenticated && <Item
                            title="Welcome"
                            to="/welcome"
                            icon={<AccessibilityIcon/>}
                            selected={selected}
                            setSelected={setSelected}
                        />}
                        {!isAuthenticated && <Item
                            title="Register"
                            to="/register"
                            icon={<AppRegistrationIcon/>}
                            selected={selected}
                            setSelected={setSelected}
                        />}
                        {!isAuthenticated && <Item
                            title="Login"
                            to="/login"
                            icon={<LoginIcon/>}
                            selected={selected}
                            setSelected={setSelected}
                        />}
                        {isAuthenticated && <Item
                            title="Dashboard"
                            to="/"
                            icon={<HomeOutlinedIcon/>}
                            selected={selected}
                            setSelected={setSelected}
                        />}

                        <Typography
                            variant="h6"
                            color={colors.grey[300]}
                            sx={{m: "15px 0 5px 20px"}}
                        >
                            Data
                        </Typography>
                        <Item
                            title="News Articles"
                            to="/news"
                            icon={<NewspaperIcon/>}
                            selected={selected}
                            setSelected={setSelected}
                        />
                        <Item
                            title="Stock Screener"
                            to="/stockScreener"
                            icon={<QueryStatsIcon/>}
                            selected={selected}
                            setSelected={setSelected}
                        />

                        {isAuthenticated && <Typography
                            variant="h6"
                            color={colors.grey[300]}
                            sx={{m: "15px 0 5px 20px"}}
                        >
                            Pages
                        </Typography>}
                        {isAuthenticated && <Item
                            title="My Portfolio"
                            to="/myPortfolio"
                            icon={<WorkIcon/>}
                            selected={selected}
                            setSelected={setSelected}
                        />}
                        {isAuthenticated && <Item
                            title="Transaction History"
                            to="/transactions"
                            icon={<ReceiptLongIcon/>}
                            selected={selected}
                            setSelected={setSelected}
                        />}

                        {isAuthenticated && <Typography
                            variant="h6"
                            color={colors.grey[300]}
                            sx={{m: "15px 0 5px 20px"}}
                        >
                            Charts
                        </Typography>}
                        {isAuthenticated && <Item
                            title="Bar Chart"
                            to="/bar"
                            icon={<BarChartOutlinedIcon/>}
                            selected={selected}
                            setSelected={setSelected}
                        />}
                        {isAuthenticated && <Item
                            title="Pie Chart"
                            to="/pie"
                            icon={<PieChartOutlineOutlinedIcon/>}
                            selected={selected}
                            setSelected={setSelected}
                        />}
                        {isAuthenticated && <Item
                            title="Line Chart"
                            to="/line"
                            icon={<TimelineOutlinedIcon/>}
                            selected={selected}
                            setSelected={setSelected}
                        />}
                    </Box>
                </Menu>
            </ProSidebar>
        </Box>
    );
}

export default Sidebar;
