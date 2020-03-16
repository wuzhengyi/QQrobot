from nonebot import on_command, CommandSession
import paramiko

__plugin_name__ = '服务器显卡查询'
__plugin_usage__ = r"""
使用指南：
nvidia [服务器名]

当前支持的服务器有：
gemini leo scorpio taurus virgo
"""

server_dict = {'gemini': '114.212.85.149',
'leo': '114.212.86.34',
'scorpio': '210.28.134.13',
'taurus':'114.212.83.168',
'virgo': '114.212.82.162'}

# on_command 装饰器将函数声明为一个命令处理器
# 这里 nvidia 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
@on_command('nvidia')
async def nvidia(session: CommandSession):
    # 从会话状态（session.state）中获取城市名称（server），如果当前不存在，则询问用户
    server = session.get('server', prompt='你想查询哪个服务器的显卡使用情况呢？')
    # 获取城市的天气预报
    nvidia_report = await get_nvidia_of_server(server)
    # 向用户发送天气预报
    await session.send(nvidia_report)


# nvidia.args_parser 装饰器将函数声明为 nvidia 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@nvidia.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state['server'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('要查询的服务器名称不能为空呢，请重新输入')

    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg


async def get_nvidia_of_server(server: str) -> str:
    # 这里简单返回一个字符串
    # 实际应用中，这里应该调用返回真实数据的天气 API，并拼接成天气预报内容 
    port = 22
    username = 'aux'  
    password = '123qwe'  
    execmd = "nvidia-smi"  
    if server in server_dict:
        out = sshclient_execmd(server_dict[server], port, username, password, execmd)
    else:
        out = '服务器不存在，请重试。'
    return out

def sshclient_execmd(hostname: str, port: int, username: str, password: str, execmd: str) -> str:   
    s = paramiko.SSHClient()  
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
      
    s.connect(hostname=hostname, port=port, username=username, password=password)  
    stdin, stdout, _ = s.exec_command (execmd)  
    stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.  
    out = stdout.read().decode(encoding = "utf-8")
    temp = out.split('\n')
    out = temp[8]+'\n'+temp[11]+'\n'+temp[14]+'\n'+temp[17]
    s.close()  
    return out
