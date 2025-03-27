import SuperTokens from "supertokens-auth-react";
import EmailPassword from "supertokens-auth-react/recipe/emailpassword";
import ThirdPartyEmailPassword from "supertokens-auth-react/recipe/thirdpartyemailpassword";
import Session from "supertokens-auth-react/recipe/session";
import { Github, Google } from "supertokens-auth-react/recipe/thirdparty";

// SuperTokens初始化配置
SuperTokens.init({
    appInfo: {
        appName: "泓泰生物科技",
        apiDomain: "http://localhost:8000",
        websiteDomain: "http://localhost:8080",
        apiBasePath: "/auth",
        websiteBasePath: "/auth"
    },
    recipeList: [
        EmailPassword.init({
            signInAndUpFeature: {
                signUpForm: {
                    formFields: [
                        {
                            id: "username",
                            label: "用户名",
                            placeholder: "请输入用户名"
                        },
                        {
                            id: "email",
                            label: "邮箱",
                            placeholder: "请输入邮箱",
                            optional: true
                        }
                    ]
                }
            }
        }),
        ThirdPartyEmailPassword.init({
            signInAndUpFeature: {
                providers: [
                    Github.init(),
                    Google.init()
                ]
            },
            style: {
                button: {
                    backgroundColor: "#24292e",
                    border: "none",
                    color: "white"
                }
            }
        }),
        Session.init()
    ]
});

// 辅助函数
export const isAuthenticated = async () => {
    return await Session.doesSessionExist();
};

export const getUserInfo = async () => {
    if (await isAuthenticated()) {
        return await Session.getUserInfo();
    }
    return null;
};

export const signOut = async () => {
    await Session.signOut();
    window.location.href = "/";
};
